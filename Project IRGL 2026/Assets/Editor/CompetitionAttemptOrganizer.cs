using UnityEditor;
using UnityEngine;

// Editor-only organizer tool. This code is excluded from player builds.
public static class CompetitionAttemptOrganizer
{
    [MenuItem("IRGL/Reset Competition Attempt (Organizer)")]
    public static void ResetAttempt()
    {
        if (EditorApplication.isPlaying)
        { Debug.LogWarning("Stop Play Mode before resetting the competition attempt."); return; }
        PlayerPrefs.DeleteKey(GameSession.AttemptKey);
        PlayerPrefs.DeleteKey(GameSession.ScoreKey);
        PlayerPrefs.Save();
        Debug.Log("Competition attempt reset by organizer. Next START allows one attempt.");
    }
}
