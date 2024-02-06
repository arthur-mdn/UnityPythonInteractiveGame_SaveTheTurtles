//CalibrationManager.cs
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using SimpleJSON; 
using System.Collections.Concurrent;


public class CalibrationManager : MonoBehaviour
{
    public GameObject wristPrefab;
    public GameObject planeGameObject;
    private GameObject[] wristInstances;
    private int maxHands = 2; // Nombre maximum de mains à gérer
    public static CalibrationManager Instance { get; private set; }
    public bool invertXAxis = true; // Inverser l'axe X du plan (pour jouer direct via webcam, sans projection)

    public float slowLerpSpeed = 150f; // Vitesse de Lerp lente
    public float fastLerpSpeed = 300f; // Vitesse de Lerp rapide
    public float distanceThreshold = 0.11f; // Seuil de distance pour basculer entre Lerp lent et rapide
    private Rigidbody[] wristRigidbodies;

   void Awake()
  {
      if (Instance == null)
      {
          Instance = this;
          wristInstances = new GameObject[maxHands];
          wristRigidbodies = new Rigidbody[maxHands];
          Vector3[] initialPositions = new Vector3[] { new Vector3(4, 0.5f, 0), new Vector3(-4, 0.5f, 0) };

          for (int i = 0; i < maxHands; i++)
          {
              wristInstances[i] = Instantiate(wristPrefab, initialPositions[i], Quaternion.identity);
              wristRigidbodies[i] = wristInstances[i].GetComponent<Rigidbody>();
              wristInstances[i].SetActive(false);
          }
      }
      else
      {
          Destroy(gameObject);
      }
  }

    void Start()
    {

        planeGameObject = GameObject.Find("InitialPlane");

        if (planeGameObject == null)
        {
            Debug.LogError("Plane GameObject not found in scene!");
        }
        Mesh mesh = planeGameObject.GetComponent<MeshFilter>().mesh;
        float planeWidth = mesh.bounds.size.x * planeGameObject.transform.localScale.x;
        float planeHeight = mesh.bounds.size.z * planeGameObject.transform.localScale.z;

        Debug.Log("Largeur du Plane: " + planeWidth);
        Debug.Log("Hauteur du Plane: " + planeHeight);
        if(UdpConnectionManager.Instance != null)
        {
            UdpConnectionManager.Instance.SendData("start_calibration");
        }
    }

    private void ResetCollider(GameObject wristInstance)
    {
        BoxCollider collider = wristInstance.GetComponent<BoxCollider>();
        if (collider != null)
        {
            collider.enabled = false;
            collider.enabled = true;
        }
    }

    public void UpdateWristPositions(JSONArray handPositions)
    {
        int index = 0;
        foreach (JSONNode pos in handPositions)
        {
            if (index >= maxHands) break;

            Vector3 targetPos = ConvertToPlanePosition(pos[0].AsFloat, pos[1].AsFloat);
            if (!wristInstances[index].activeSelf) wristInstances[index].SetActive(true);

            float distance = Vector3.Distance(wristInstances[index].transform.position, targetPos);
            float lerpFactor = distance > distanceThreshold ? fastLerpSpeed : slowLerpSpeed;
            Vector3 newPosition = Vector3.Lerp(wristInstances[index].transform.position, targetPos, lerpFactor * Time.deltaTime);

            wristRigidbodies[index].MovePosition(newPosition);

            index++;
        }

        // Désactiver les GameObjects inutilisés
        for (int i = index; i < maxHands; i++)
        {
            wristInstances[i].SetActive(false);
        }
    }


    private Vector3 ConvertToPlanePosition(float x, float y)
    {
        planeGameObject = GameObject.Find("InitialPlane");

        if (planeGameObject == null)
        {
            Debug.LogError("Plane GameObject not found in scene!");
        }
        Mesh mesh = planeGameObject.GetComponent<MeshFilter>().mesh;
        float planeWidth = mesh.bounds.size.x * planeGameObject.transform.localScale.x;
        float planeHeight = mesh.bounds.size.z * planeGameObject.transform.localScale.z;

        if (invertXAxis) x = 1 - x; // Inverser l'axe X

        y = 1 - y; // Inverser l'axe Y

        // Conversion des coordonnées
        float posX = (x * planeWidth) - (planeWidth / 2f);
        float posY = (y * planeHeight) - (planeHeight / 2f);

        return new Vector3(posX, 0.5f, posY); // Position ajustée sur le plan
    }
}

