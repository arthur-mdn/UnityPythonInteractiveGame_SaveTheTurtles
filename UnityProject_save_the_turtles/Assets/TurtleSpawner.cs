using System.Collections;
using UnityEngine;

public class TurtleSpawner : MonoBehaviour
{
    public GameObject turtlePrefab;
    public GameObject particlePrefab;
    public Transform[] spawnPoints;
    public float spawnInterval = 2f; // Intervalle entre chaque apparition de tortue
    public float particleDuration = 1f; // Durée d'exécution du système de particules avant de faire apparaître la tortue

    private void Start()
    {
        StartCoroutine(SpawnTurtles());
    }

    private IEnumerator SpawnTurtles()
    {
        while (!GameManager.Instance.Gameover) // Continuer tant que le jeu n'est pas fini
        {
            yield return new WaitForSeconds(spawnInterval); // Attendre un intervalle avant de faire apparaître la prochaine tortue

            // Sélectionner un point de spawn aléatoire
            int spawnIndex = Random.Range(0, spawnPoints.Length);
            Transform spawnPoint = spawnPoints[spawnIndex];

            // Faire apparaître le ParticlePrefab à ce point
            GameObject particleInstance = Instantiate(particlePrefab, spawnPoint.position, spawnPoint.rotation);
            particleInstance.transform.rotation = Quaternion.Euler(new Vector3(-90, 0, 0)); // Oriente les particules vers le haut

            // Attendre que le ParticleSystem se termine
            yield return new WaitForSeconds(particleDuration);

            // Vérifier à nouveau si le jeu est fini avant de faire apparaître une tortue
            if (!GameManager.Instance.Gameover)
            {
                Instantiate(turtlePrefab, spawnPoint.position, spawnPoint.rotation);
            }

            // Détruire le ParticlePrefab
            Destroy(particleInstance);
        }
    }
}
