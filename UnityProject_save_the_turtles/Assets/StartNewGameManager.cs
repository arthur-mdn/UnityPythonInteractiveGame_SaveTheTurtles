using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StartNewGameManager : MonoBehaviour
{
   void Start()
   {
       if (UdpConnectionManager.Instance != null)
       {
           UdpConnectionManager.Instance.SendData("start_yolo_hands_detection_to_launch_new_game");
       }
   }
}
