using UnityEngine;
using System.Collections;

public class ShowStartCalibration : MonoBehaviour
{
    public GameObject calibrateOkObject;
    public GameObject calibrateFailedObject;
    public GameObject calibrationBall;
    private Rigidbody calibrationBallRigidbody;

    void Start()
    {
        // Initialiser la variable d'instance calibrationBallRigidbody
        calibrationBallRigidbody = calibrationBall.GetComponent<Rigidbody>();
        if (calibrationBallRigidbody != null)
        {
            calibrationBallRigidbody.isKinematic = true; // Désactiver temporairement la physique
        }
    }

    public void StartCalibrateOkDisplay()
    {
        StartCoroutine(ShowCalibrateOkTemporarily());
    }

    IEnumerator ShowCalibrateOkTemporarily()
    {
        if (calibrateOkObject != null)
        {
            // Activer l'objet CalibrateOk
            calibrateOkObject.SetActive(true);

            // Attendre pendant un certain délai
            yield return new WaitForSeconds(5f);

            // Désactiver l'objet CalibrateOk
            calibrateOkObject.SetActive(false);

            // Réactiver la physique de la balle de calibration
            if (calibrationBallRigidbody != null)
            {
                calibrationBallRigidbody.isKinematic = false;
            }
        }
        else
        {
            Debug.LogError("L'objet CalibrateOk n'est pas assigné dans l'inspecteur.");
        }
    }

    // Méthode publique pour démarrer l'affichage temporaire de CalibrateOk
    public void StartCalibrateFailedDisplay()
    {
        if (calibrateFailedObject != null)
        {
            // Activer l'objet CalibrateFailed
            calibrateFailedObject.SetActive(true);
        }
    }

}
