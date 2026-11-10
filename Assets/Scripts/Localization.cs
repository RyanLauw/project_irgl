using System;
using UnityEngine;

public static class Localization
{
    public static bool English { get; private set; }
    public static event Action Changed;
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    static void Reset() { English = PlayerPrefs.GetInt("IRGL.Language", 0) == 1; Changed = null; }
    public static string Text(string id, string en) { return English ? en : id; }
    public static void Toggle()
    {
        English = !English;
        PlayerPrefs.SetInt("IRGL.Language", English ? 1 : 0);
        PlayerPrefs.Save();
        if (Changed != null) Changed();
    }
}
