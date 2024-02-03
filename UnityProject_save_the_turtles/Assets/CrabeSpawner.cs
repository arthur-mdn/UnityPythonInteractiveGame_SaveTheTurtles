using System.Collections;
using UnityEngine;

public class CrabeSpawner : MonoBehaviour
{
    public GameObject crabePrefab;
    public Transform[] spawnPoints;
    public float spawnInterval = 1f; // Intervalle en secondes entre chaque apparition de crabe

    private void Start()
    {
        StartCoroutine(SpawnCrabes());
    }

    private IEnumerator SpawnCrabes()
    {
        while (true) // Boucle infinie pour continuer à faire apparaître des crabes
        {
            yield return new WaitForSeconds(spawnInterval); // Attendre un intervalle avant de faire apparaître le prochain crabe

            // Sélectionner un point de spawn aléatoire
            int spawnIndex = Random.Range(0, spawnPoints.Length);
            Transform spawnPoint = spawnPoints[spawnIndex];

            // Faire apparaître un crabe à ce point
            Instantiate(crabePrefab, spawnPoint.position, spawnPoint.rotation);
            Debug.DrawRay(spawnPoint.position, Vector3.up * 2, Color.red, 2f);

        }
    }
}
