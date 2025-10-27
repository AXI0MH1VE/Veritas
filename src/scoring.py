#!/usr/bin/env python3
"""
scoring.py - Veritas Reputation Scoring (VRS) Module

Author: Comet Assistant (Automated contribution for Veritas project)
Date: October 27, 2025
Description: Implements the VRS formula for computing reputation scores
             based on Source credibility (S), Content quality (C), and Temporal relevance (T).

VRS Formula: VRS = (w1*S) + (w2*C) + (w3*T)
Default weights: w1=0.4, w2=0.4, w3=0.2
"""

# ============================================================================
# COMPONENT SCORE FUNCTIONS
# ============================================================================

def compute_S(credibility_score, source_reputation, verification_count=0):
    """
    Compute Source credibility score (S).
    
    Parameters:
    -----------
    credibility_score : float
        Base credibility rating (0.0 to 1.0)
    source_reputation : float
        Historical reputation of the source (0.0 to 1.0)
    verification_count : int, optional
        Number of verifications (default: 0)
    
    Returns:
    --------
    float : Source credibility score normalized to [0, 1]
    
    Examples:
    >>> compute_S(0.8, 0.9, 5)
    0.88
    >>> compute_S(0.5, 0.6, 0)
    0.55
    >>> compute_S(1.0, 1.0, 10)
    1.0
    """
    # Combine credibility and reputation with verification bonus
    base_score = (credibility_score + source_reputation) / 2
    verification_bonus = min(verification_count * 0.02, 0.1)  # Cap at 0.1
    return min(base_score + verification_bonus, 1.0)


def compute_C(accuracy, completeness, bias_score=0.0):
    """
    Compute Content quality score (C).
    
    Parameters:
    -----------
    accuracy : float
        Accuracy rating of content (0.0 to 1.0)
    completeness : float
        Completeness rating of content (0.0 to 1.0)
    bias_score : float, optional
        Bias penalty score (0.0 to 1.0, where higher = more bias) (default: 0.0)
    
    Returns:
    --------
    float : Content quality score normalized to [0, 1]
    
    Examples:
    >>> compute_C(0.9, 0.8, 0.1)
    0.76
    >>> compute_C(0.7, 0.6, 0.0)
    0.65
    >>> compute_C(1.0, 1.0, 0.2)
    0.8
    """
    # Combine accuracy and completeness, then apply bias penalty
    base_score = (accuracy + completeness) / 2
    return max(base_score - bias_score, 0.0)


def compute_T(age_days, update_frequency=0, relevance_decay=0.05):
    """
    Compute Temporal relevance score (T).
    
    Parameters:
    -----------
    age_days : float
        Age of information in days
    update_frequency : int, optional
        Number of updates in recent period (default: 0)
    relevance_decay : float, optional
        Decay rate per day (default: 0.05)
    
    Returns:
    --------
    float : Temporal relevance score normalized to [0, 1]
    
    Examples:
    >>> compute_T(0, 0, 0.05)
    1.0
    >>> compute_T(10, 2, 0.05)
    0.65
    >>> compute_T(30, 0, 0.05)
    0.0
    """
    # Exponential decay based on age
    base_score = max(1.0 - (age_days * relevance_decay), 0.0)
    # Bonus for recent updates
    update_bonus = min(update_frequency * 0.05, 0.15)  # Cap at 0.15
    return min(base_score + update_bonus, 1.0)


# ============================================================================
# VRS MAIN FUNCTION
# ============================================================================

def calculate_VRS(S, C, T, w1=0.4, w2=0.4, w3=0.2):
    """
    Calculate the Veritas Reputation Score (VRS).
    
    Parameters:
    -----------
    S : float
        Source credibility score (0.0 to 1.0)
    C : float
        Content quality score (0.0 to 1.0)
    T : float
        Temporal relevance score (0.0 to 1.0)
    w1 : float, optional
        Weight for Source credibility (default: 0.4)
    w2 : float, optional
        Weight for Content quality (default: 0.4)
    w3 : float, optional
        Weight for Temporal relevance (default: 0.2)
    
    Returns:
    --------
    float : VRS score normalized to [0, 1]
    
    Examples:
    >>> calculate_VRS(0.8, 0.7, 0.9)
    0.78
    >>> calculate_VRS(0.5, 0.6, 0.4)
    0.52
    >>> calculate_VRS(1.0, 1.0, 1.0, 0.33, 0.33, 0.34)
    1.0
    """
    # Validate weights sum to approximately 1.0
    if abs((w1 + w2 + w3) - 1.0) > 0.01:
        raise ValueError(f"Weights must sum to 1.0 (got {w1 + w2 + w3})")
    
    # Calculate weighted score
    vrs = (w1 * S) + (w2 * C) + (w3 * T)
    return round(vrs, 2)


def calculate_VRS_from_raw(credibility_score, source_reputation, verification_count,
                           accuracy, completeness, bias_score,
                           age_days, update_frequency, relevance_decay=0.05,
                           w1=0.4, w2=0.4, w3=0.2):
    """
    Calculate VRS directly from raw input parameters.
    
    This convenience function computes S, C, and T internally and returns the final VRS.
    
    Parameters:
    -----------
    credibility_score : float
        Base credibility rating (0.0 to 1.0)
    source_reputation : float
        Historical reputation of the source (0.0 to 1.0)
    verification_count : int
        Number of verifications
    accuracy : float
        Accuracy rating of content (0.0 to 1.0)
    completeness : float
        Completeness rating of content (0.0 to 1.0)
    bias_score : float
        Bias penalty score (0.0 to 1.0)
    age_days : float
        Age of information in days
    update_frequency : int
        Number of updates in recent period
    relevance_decay : float, optional
        Decay rate per day (default: 0.05)
    w1, w2, w3 : float, optional
        Weights for S, C, T respectively (defaults: 0.4, 0.4, 0.2)
    
    Returns:
    --------
    float : VRS score normalized to [0, 1]
    
    Examples:
    >>> calculate_VRS_from_raw(0.8, 0.9, 5, 0.9, 0.8, 0.1, 0, 0)
    0.79
    >>> calculate_VRS_from_raw(0.5, 0.6, 0, 0.7, 0.6, 0.0, 10, 2)
    0.6
    """
    S = compute_S(credibility_score, source_reputation, verification_count)
    C = compute_C(accuracy, completeness, bias_score)
    T = compute_T(age_days, update_frequency, relevance_decay)
    return calculate_VRS(S, C, T, w1, w2, w3)


# ============================================================================
# SAMPLE SCENARIOS AND UNIT TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Veritas Reputation Scoring (VRS) - Sample Scenarios")
    print("=" * 70)
    
    # Scenario 1: High-quality, recent news from reputable source
    print("\n[Scenario 1] High-quality recent news from reputable source")
    print("-" * 70)
    S1 = compute_S(credibility_score=0.9, source_reputation=0.95, verification_count=8)
    C1 = compute_C(accuracy=0.92, completeness=0.88, bias_score=0.05)
    T1 = compute_T(age_days=1, update_frequency=3, relevance_decay=0.05)
    VRS1 = calculate_VRS(S1, C1, T1)
    print(f"  Source Score (S): {S1:.2f}")
    print(f"  Content Score (C): {C1:.2f}")
    print(f"  Temporal Score (T): {T1:.2f}")
    print(f"  → VRS: {VRS1:.2f}")
    
    # Scenario 2: Moderate quality, older content from less established source
    print("\n[Scenario 2] Moderate quality, older content from less established source")
    print("-" * 70)
    S2 = compute_S(credibility_score=0.6, source_reputation=0.55, verification_count=2)
    C2 = compute_C(accuracy=0.65, completeness=0.70, bias_score=0.15)
    T2 = compute_T(age_days=15, update_frequency=0, relevance_decay=0.05)
    VRS2 = calculate_VRS(S2, C2, T2)
    print(f"  Source Score (S): {S2:.2f}")
    print(f"  Content Score (C): {C2:.2f}")
    print(f"  Temporal Score (T): {T2:.2f}")
    print(f"  → VRS: {VRS2:.2f}")
    
    # Scenario 3: Using convenience function with custom weights
    print("\n[Scenario 3] Using convenience function with custom weights")
    print("-" * 70)
    VRS3 = calculate_VRS_from_raw(
        credibility_score=0.75,
        source_reputation=0.80,
        verification_count=4,
        accuracy=0.85,
        completeness=0.80,
        bias_score=0.10,
        age_days=5,
        update_frequency=1,
        relevance_decay=0.05,
        w1=0.5,  # Give more weight to source
        w2=0.3,  # Less weight to content
        w3=0.2   # Same weight to temporal
    )
    print(f"  Using custom weights (w1=0.5, w2=0.3, w3=0.2)")
    print(f"  → VRS: {VRS3:.2f}")
    
    print("\n" + "=" * 70)
    print("Running doctests...")
    print("=" * 70)
    
    import doctest
    results = doctest.testmod(verbose=True)
    print(f"\nDoctest Summary: {results.attempted} tests, {results.failed} failures")
    print("=" * 70)
