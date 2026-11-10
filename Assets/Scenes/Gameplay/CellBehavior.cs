using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

[RequireComponent(typeof(Image))]
public class CellBehavior : MonoBehaviour, IPointerDownHandler, IPointerEnterHandler, IDragHandler
{
    public int gridX, gridY;
    private Image cellImage;
    private GridManager game;
    public void Bind(GridManager manager) { game = manager; }
    public void SetVisual(Color color)
    {
        if (cellImage == null) cellImage = GetComponent<Image>();
        cellImage.color = color;
    }
    public void OnPointerDown(PointerEventData data)
    {
        if (game == null) return;
        if (data.button != PointerEventData.InputButton.Left && data.button != PointerEventData.InputButton.Right) return;
        game.BeginStroke();
        game.PaintCell(gridX, gridY, data.button == PointerEventData.InputButton.Right);
    }
    public void OnPointerEnter(PointerEventData data)
    {
        if (game == null) return;
        if (Input.GetMouseButton(0)) game.PaintCell(gridX, gridY, false);
        else if (Input.GetMouseButton(1)) game.PaintCell(gridX, gridY, true);
    }
    public void OnDrag(PointerEventData data) { } // retain drag ownership while pointer enters other cells
}
