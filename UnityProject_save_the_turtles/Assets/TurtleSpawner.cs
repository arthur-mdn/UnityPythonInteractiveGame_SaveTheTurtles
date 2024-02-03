using System.Collections;
using UnityEngine;

public class TurtleSpawner : MonoBehaviour
{
    public GameObject turtlePrefab; // Assignez votre prefab de tortue ici dans l'inspecteur
    public Transform[] spawnPoints; // Assignez vos points de spawn ici dans l'inspecteur
    public float spawnInterval = 3f; // Intervalle en secondes entre chaque apparition de tortue

    private void Start()
    {
        StartCoroutine(SpawnTurtles());
    }

    private IEnumerator SpawnTurtles()
    {
        while (true) // Boucle infinie pour continuer à faire apparaître des tortues
        {
            yield return new WaitForSeconds(spawnInterval); // Attendre un intervalle avant de faire apparaître la prochaine tortue

            // Sélectionner un point de spawn aléatoire
            int spawnIndex = Random.Range(0, spawnPoints.Length);
            Transform spawnPoint = spawnPoints[spawnIndex];

            // Faire apparaître une tortue à ce point
            Instantiate(turtlePrefab, spawnPoint.position, spawnPoint.rotation);
        }
    }
}
