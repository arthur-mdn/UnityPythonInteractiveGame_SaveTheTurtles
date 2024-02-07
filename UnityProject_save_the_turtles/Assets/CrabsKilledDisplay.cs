using UnityEngine;
using TMPro;

public class CrabsKilledDisplay : MonoBehaviour
{
    public TMP_Text crabsKilledText;

    private void Update()
    {
        if (GameManager.Instance != null)
        {
            crabsKilledText.text = "" + GameManager.Instance.CrabsKilled;
        }
    }
}
