using UnityEngine;

[CreateAssetMenu(fileName = "CompetitionScoring", menuName = "IRGL/Competition Scoring")]
public class ScoreSettings : ScriptableObject
{
    [Header("Points awarded once when a level is solved")]
    [Min(0)] public int level1Points = 200;
    [Min(0)] public int level2Points = 300;
    [Min(0)] public int level3Points = 500;
    public int[] Snapshot()
    { return new[] { Mathf.Max(0,level1Points), Mathf.Max(0,level2Points), Mathf.Max(0,level3Points) }; }
}
