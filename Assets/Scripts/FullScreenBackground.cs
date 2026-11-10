using UnityEngine;
using UnityEngine.UI;

// The Image exists in the scene. Only resize it to cover any screen aspect ratio.
[ExecuteAlways, RequireComponent(typeof(Image))]
public class FullScreenBackground : MonoBehaviour
{
    RectTransform rect, parent;
    Image image;
    Vector2 lastParentSize, lastSpriteSize;
    void OnEnable()
    {
        rect = GetComponent<RectTransform>(); parent = transform.parent as RectTransform;
        image = GetComponent<Image>();
        rect.anchorMin = rect.anchorMax = rect.pivot = new Vector2(.5f, .5f);
        rect.anchoredPosition = Vector2.zero;
        image.preserveAspect = false; image.raycastTarget = false;
        lastParentSize = lastSpriteSize = Vector2.zero;
        Fit();
    }
    void Update() { Fit(); }
    void Fit()
    {
        if (parent == null || image == null || image.sprite == null) return;
        Vector2 available = parent.rect.size, source = image.sprite.rect.size;
        if (available == lastParentSize && source == lastSpriteSize) return;
        if (source.x <= 0 || source.y <= 0 || available.x <= 0 || available.y <= 0) return;
        lastParentSize = available; lastSpriteSize = source;
        float scale = Mathf.Max(available.x / source.x, available.y / source.y);
        rect.sizeDelta = source * scale;
    }
}
