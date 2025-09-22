# Install necessary libraries if you haven't already
# pip install pandas scikit-learn

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier
from set_to_set import gower_distance_matrix

class diff_guidance:
    """
    Implements the Differential Guidance (DG) technique with multiple
    threshold methods for interpreting results.
    """
    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        self.df = df.copy()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.numerical_cols = self.df.select_dtypes(include=np.number).columns.tolist()
        self._precompute_distribution_thresholds()

    def _precompute_distribution_thresholds(self, n_samples=100, quantile=0.75):
        """
        Pre-computes a distribution-based threshold for each numerical outcome
        to determine what a "high" difference is for this dataset.
        """
        self.distribution_thresholds = {}
        for col in self.numerical_cols:
            differences = []
            for _ in range(n_samples):
                # Take two random samples of 20% of the data
                sample1 = self.df[col].sample(frac=0.2, replace=True)
                sample2 = self.df[col].sample(frac=0.2, replace=True)
                differences.append(abs(sample1.mean() - sample2.mean()))
            
            self.distribution_thresholds[col] = np.quantile(differences, quantile)

    # Gower distance matrix now imported from set_to_set.py

    def _get_subsets(self, predicate_col, predicate_val):
        """Partitions the data into Included, Counterfactual, and Remainder."""
        included_mask = self.df[predicate_col] == predicate_val
        D_i = self.df[included_mask]
        if D_i.empty:
            raise ValueError(f"No data found for filter '{predicate_col} == {predicate_val}'.")

        candidates = self.df[~included_mask]
        features_to_match = [col for col in self.df.columns if col != predicate_col]
        dist_matrix = gower_distance_matrix(D_i[features_to_match], candidates[features_to_match], self.numerical_cols, self.categorical_cols)
        nearest_indices = np.argmin(dist_matrix, axis=1)
        counterfactual_indices = candidates.index[nearest_indices]
        D_c = candidates.loc[counterfactual_indices]

        remainder_mask = ~self.df.index.isin(D_i.index) & ~self.df.index.isin(D_c.index)
        D_r = self.df[remainder_mask]
        return D_i, D_c, D_r

    def _detect_confounders(self, D_c, D_r, ignored_cols):
        """Identifies the most likely confounding variable."""
        combined_df = pd.concat([D_c, D_r])
        y = np.array([1] * len(D_c) + [0] * len(D_r))
        X = combined_df.drop(columns=ignored_cols)
        X = pd.get_dummies(X, drop_first=True)
        
        clf = DecisionTreeClassifier(max_depth=3, random_state=42)
        clf.fit(X, y)
        
        importances = pd.Series(clf.feature_importances_, index=X.columns)
        top_confounder = importances.sort_values(ascending=False).index[0]
        return top_confounder.split('_')[0]

    def _diff_guidance_score(self, predicate_col, predicate_val, included_variables=None):
        """
        Computes Differential Guidance similarity scores using Gower distance, following cf_guidance logic.
        S1_Potential_Effect: similarity between Di and Dc
        S2_Confounding_Signal: similarity between Dc and Dr
        Args:
            predicate_col: column to filter
            predicate_val: value to filter
            included_variables: list of columns to include (default: all except predicate_col)
        Returns:
            dict with S1_Potential_Effect, S2_Confounding_Signal
        """
        D_i, D_c, D_r = self._get_subsets(predicate_col, predicate_val)
        
        if included_variables is None:
            included_variables = [col for col in self.df.columns if col != predicate_col]
            
        # Helper to compute mean Gower similarity between two sets
        def mean_gower_similarity(A, B):
            dm = gower_distance_matrix(A[included_variables], B[included_variables], self.numerical_cols, self.categorical_cols)
            # Similarity is 1 - distance
            return np.mean(1 - dm)
        
        S1_Potential_Effect = mean_gower_similarity(D_i, D_c)
        S2_Confounding_Signal = mean_gower_similarity(D_c, D_r)
        
        return {
            "S1_Potential_Effect": S1_Potential_Effect,
            "S2_Confounding_Signal": S2_Confounding_Signal
        }
        
    def compute_guidance(self, predicate_col, predicate_val, outcome_col, included_col=None,
                         method='distribution', alpha=1.0):
        """
        The main method to compute DG scores and detect confounders.

        Args:
            ...
            method (str): The threshold method to use: 'relative' or 'distribution'.
            alpha (float): The sensitivity parameter for the 'relative' method.
                           A higher alpha requires a stronger confounding signal to trigger a warning.
        """
        D_i, D_c, D_r = self._get_subsets(predicate_col, predicate_val)
        
        s1, s2 = self._diff_guidance_score(self, predicate_col, predicate_val, included_col)
        
        result = {
            "Potential_Effect": s1,
            "Confounding_Signal": s2,
            "interpretation": "",
            "suggested_confounder": None
        }

        # --- Interpretation Logic with Multiple Methods ---
        is_confounded = False
        if method == 'relative':
            if s2 > alpha * s1:
                is_confounded = True
                result["interpretation"] = f"⚠️ High Risk of Confounding (S2 > {alpha} * S1)."
            else:
                result["interpretation"] = "✅ Low confounding risk based on relative comparison."

        elif method == 'distribution':
            threshold = self.distribution_thresholds.get(outcome_col)
            if threshold is None:
                raise ValueError(f"Outcome column '{outcome_col}' is not numerical and has no pre-computed threshold.")
            
            if s2 > threshold:
                is_confounded = True
                result["interpretation"] = f"⚠️ High Risk of Confounding (S2 > dataset threshold of {threshold:.4f})."
            else:
                 result["interpretation"] = "✅ Low confounding risk based on distribution threshold."
        
        else:
            raise ValueError("Method must be 'relative' or 'distribution'.")

        if is_confounded:
            result["suggested_confounder"] = self._detect_confounders(D_c, D_r, [predicate_col, outcome_col])
             
        return result
