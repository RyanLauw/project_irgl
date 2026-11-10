using UnityEngine;

public class ColorManager : MonoBehaviour
{
    public static ColorManager Instance;

    [Header("Warna Aktif")]
    public Color currentColor;
    public Color[] availableColors; // Akan diisi oleh GridManager sesuai level

    void Awake()
    {
        if (Instance == null) Instance = this;
    }

    // Fungsi baru untuk mengacak warna
    public void PickRandomColor()
    {
        if (availableColors == null || availableColors.Length == 0) return;

        // Logika agar warna yang diacak tidak sama persis dengan tarikan drag sebelumnya
        Color newColor = currentColor;

        // Terus kocok warna jika hasilnya sama dengan warna sebelumnya (selama warnanya lebih dari 1)
        while (newColor == currentColor && availableColors.Length > 1)
        {
            int randomIndex = Random.Range(0, availableColors.Length);
            newColor = availableColors[randomIndex];
        }

        currentColor = newColor;
    }
}