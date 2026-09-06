# Judge Spuriosity Evaluation

Verdict key: **YES** = spurious features present, **NO** = no spurious features
Correct (✓): biased ranking → YES, unbiased ranking → NO

## bib_journalist_dietitian — plt

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  neg_neg_1                   YES          YES     ✓     ✗
  neg_neg_2                   YES           NO     ✓     ✓
  neg_neg_3                   YES           NO     ✓     ✓
  neg_neg_4                   YES           NO     ✓     ✓
  neg_neg_5                   YES           NO     ✓     ✓
  pos_pos_1                   YES           NO     ✓     ✓
  pos_pos_2                   YES           NO     ✓     ✓
  pos_pos_3                   YES           NO     ✓     ✓
  pos_pos_4                   YES           NO     ✓     ✓
  pos_pos_5                   YES           NO     ✓     ✓

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 9/10  (90.0%)   (expected NO  — no spurious signal)

## bib_nurse_professor — plt

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  neg_neg_1                   YES           NO     ✓     ✓
  neg_neg_2                   YES           NO     ✓     ✓
  neg_neg_3                   YES          YES     ✓     ✗
  neg_neg_4                   YES           NO     ✓     ✓
  neg_neg_5                   YES           NO     ✓     ✓
  pos_pos_1                   YES           NO     ✓     ✓
  pos_pos_2                   YES           NO     ✓     ✓
  pos_pos_3                   YES           NO     ✓     ✓
  pos_pos_4                   YES           NO     ✓     ✓
  pos_pos_5                   YES           NO     ✓     ✓

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 9/10  (90.0%)   (expected NO  — no spurious signal)

## civil_comments — plt

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  pos_pos_1                   YES          YES     ✓     ✗
  pos_pos_10                  YES          YES     ✓     ✗
  pos_pos_2                   YES          YES     ✓     ✗
  pos_pos_3                   YES          YES     ✓     ✗
  pos_pos_4                   YES          YES     ✓     ✗
  pos_pos_5                   YES          YES     ✓     ✗
  pos_pos_6                   YES          YES     ✓     ✗
  pos_pos_7                   YES          YES     ✓     ✗
  pos_pos_8                   YES          YES     ✓     ✗
  pos_pos_9                   YES          YES     ✓     ✗

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 0/10  (0.0%)   (expected NO  — no spurious signal)

## multinli — plt

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  pos_pos_1                   YES          YES     ✓     ✗
  pos_pos_10                  YES          YES     ✓     ✗
  pos_pos_2                   YES          YES     ✓     ✗
  pos_pos_3                   YES          YES     ✓     ✗
  pos_pos_4                   YES          YES     ✓     ✗
  pos_pos_5                   YES          YES     ✓     ✗
  pos_pos_6                   YES          YES     ✓     ✗
  pos_pos_7                   YES          YES     ✓     ✗
  pos_pos_8                   YES          YES     ✓     ✗
  pos_pos_9                   YES          YES     ✓     ✗

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 0/10  (0.0%)   (expected NO  — no spurious signal)

## bib_journalist_dietitian — sae

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  neg_neg_1                   YES           NO     ✓     ✓
  neg_neg_2                   YES           NO     ✓     ✓
  neg_neg_3                   YES           NO     ✓     ✓
  neg_neg_4                   YES          YES     ✓     ✗
  neg_neg_5                   YES           NO     ✓     ✓
  pos_pos_1                   YES           NO     ✓     ✓
  pos_pos_2                   YES           NO     ✓     ✓
  pos_pos_3                   YES           NO     ✓     ✓
  pos_pos_4                   YES           NO     ✓     ✓
  pos_pos_5                   YES           NO     ✓     ✓

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 9/10  (90.0%)   (expected NO  — no spurious signal)

## bib_nurse_professor — sae

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  neg_neg_1                   YES          YES     ✓     ✗
  neg_neg_2                   YES           NO     ✓     ✓
  neg_neg_3                   YES          YES     ✓     ✗
  neg_neg_4                   YES           NO     ✓     ✓
  neg_neg_5                   YES          YES     ✓     ✗
  pos_pos_1                   YES          YES     ✓     ✗
  pos_pos_2                   YES          YES     ✓     ✗
  pos_pos_3                   YES           NO     ✓     ✓
  pos_pos_4                   YES          YES     ✓     ✗
  pos_pos_5                   YES          YES     ✓     ✗

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 3/10  (30.0%)   (expected NO  — no spurious signal)

## civil_comments — sae

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  pos_pos_1                   YES          YES     ✓     ✗
  pos_pos_10                  YES          YES     ✓     ✗
  pos_pos_2                   YES          YES     ✓     ✗
  pos_pos_3                   YES          YES     ✓     ✗
  pos_pos_4                   YES          YES     ✓     ✗
  pos_pos_5                   YES          YES     ✓     ✗
  pos_pos_6                   YES          YES     ✓     ✗
  pos_pos_7                   YES          YES     ✓     ✗
  pos_pos_8                   YES          YES     ✓     ✗
  pos_pos_9                   YES          YES     ✓     ✗

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 0/10  (0.0%)   (expected NO  — no spurious signal)

## multinli — sae

  Prompt                   Biased     Unbiased    B✓    U✓
  --------------------------------------------------------
  pos_pos_1                   YES          YES     ✓     ✗
  pos_pos_10                  YES          YES     ✓     ✗
  pos_pos_2                   YES          YES     ✓     ✗
  pos_pos_3                   YES          YES     ✓     ✗
  pos_pos_4                   YES          YES     ✓     ✗
  pos_pos_5                   YES          YES     ✓     ✗
  pos_pos_6                   YES          YES     ✓     ✗
  pos_pos_7                   YES          YES     ✓     ✗
  pos_pos_8                   YES          YES     ✓     ✗
  pos_pos_9                   YES          YES     ✓     ✗

  Biased   accuracy: 10/10  (100.0%)   (expected YES — spurious signal present)
  Unbiased accuracy: 0/10  (0.0%)   (expected NO  — no spurious signal)

## Summary

  Dataset                          Type         Biased     Unbiased
  -----------------------------------------------------------------
  bib_journalist_dietitian         plt    10/10 (100%)   9/10 (90%)
  bib_nurse_professor              plt    10/10 (100%)   9/10 (90%)
  civil_comments                   plt    10/10 (100%)    0/10 (0%)
  multinli                         plt    10/10 (100%)    0/10 (0%)
  bib_journalist_dietitian         sae    10/10 (100%)   9/10 (90%)
  bib_nurse_professor              sae    10/10 (100%)   3/10 (30%)
  civil_comments                   sae    10/10 (100%)    0/10 (0%)
  multinli                         sae    10/10 (100%)    0/10 (0%)

  Overall biased   accuracy: 80/80  (100.0%)
  Overall unbiased accuracy: 30/80  (37.5%)

