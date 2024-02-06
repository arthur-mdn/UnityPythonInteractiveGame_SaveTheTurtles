using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.Collections;

public class RestartProgress : MonoBehaviour
{
    public Image progressBar;
    private float fillAmount = 0f;
    public float fillSpeed = 0.5f;
    private bool isWristInContact = false;

    private void Update()
    {
        progressBar.fillAmount = fillAmount; // Assurez-vous de mettre à jour la barre de progression dans Update
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Wrist"))
        {
            isWristInContact = true;
            Debug.Log("Wrist entered");
            if (fillAmount < 1.0f) // Commencer à remplir seulement si la barre n'est pas déjà pleine
            {
                StopAllCoroutines(); // Arrêter toutes les coroutines en cours
                StartCoroutine(FillProgress()); // Commencer à remplir la barre
            }
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.CompareTag("Wrist"))
        {
            isWristInContact = true; // Confirmer que le Wrist est toujours en contact
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Wrist"))
        {
            isWristInContact = false; // Le Wrist a quitté le collider
            Debug.Log("Wrist exited");
            if (fillAmount > 0f) // Commencer à drainer seulement si la barre n'est pas déjà vide
            {
                StopAllCoroutines(); // Arrêter toutes les coroutines en cours
                StartCoroutine(DrainProgress()); // Commencer à drainer la barre
            }
        }
    }

    private IEnumerator FillProgress()
    {
        while (fillAmount < 1.0f)
        {
            fillAmount += Time.deltaTime * fillSpeed;
            yield return null;
        }

        // Recharger la scène ici, une fois que la barre est pleine
        Debug.Log("Restarting scene");
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

    private IEnumerator DrainProgress()
    {
        while (fillAmount > 0f && !isWristInContact) // Assurez-vous de drainer seulement si le Wrist n'est pas en contact
        {
            fillAmount -= Time.deltaTime * fillSpeed * 2;
            yield return null;
        }
    }
}
