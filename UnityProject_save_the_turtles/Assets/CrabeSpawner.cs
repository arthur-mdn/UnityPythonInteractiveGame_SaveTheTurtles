using System.Collections;
using UnityEngine;

public class CrabeSpawner : MonoBehaviour
{
    public GameObject crabePrefab;
    public Transform[] spawnPoints;
    public float spawnInterval = 10f; // Intervalle initial en secondes entre chaque apparition de crabe
    public float minimumSpawnInterval = 0.5f; // Intervalle minimum de spawn pour éviter une fréquence trop élevée
    public float spawnAcceleration = 0.5f; // Diminution de l'intervalle de spawn après chaque crabe

    private void Start()
    {
        StartCoroutine(SpawnCrabes());
    }

    private IEnumerator SpawnCrabes()
    {
        while (true)
        {
            yield return new WaitForSeconds(spawnInterval);

            // Sélectionner un point de spawn aléatoire
            int spawnIndex = Random.Range(0, spawnPoints.Length);
            Transform spawnPoint = spawnPoints[spawnIndex];

            // Faire apparaître un crabe à ce point
            Instantiate(crabePrefab, spawnPoint.position, spawnPoint.rotation);
            Debug.DrawRay(spawnPoint.position, Vector3.up * 2, Color.red, 2f);

            // Réduire l'intervalle de spawn, sans descendre en dessous du minimum défini
            spawnInterval = Mathf.Max(spawnInterval - spawnAcceleration, minimumSpawnInterval);
        }
    }
}
