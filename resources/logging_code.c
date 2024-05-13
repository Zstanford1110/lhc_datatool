using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using AptabaseSDK;

public class NetworkManager : MonoBehaviour
{
    public static NetworkManager Instance;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else if (Instance != this)
        {
            Destroy(gameObject);
        }
    }

    public IEnumerator SendDataToServer(AnalyticsData analyticsData, bool applicationClose)
    {
        WaitForSecondsRealtime cachedAnalytics = new WaitForSecondsRealtime(0.05f);
        Aptabase.TrackEvent("Player Death", new Dictionary<string, object>
        {
            {"Wave That Player Died On", analyticsData.analyticsDataRunData.wavePlayerDiedOn.ToString()},
            {"Wave Type That Player Died On", analyticsData.analyticsDataRunData.waveTypePlayerDiedOn},
            {"Enemy That Killed Player", analyticsData.analyticsDataRunData.enemyThatKilledPlayer}
        });

        Aptabase.TrackEvent("Amount Of Time Per Run", new Dictionary<string, object>
        {
            {"Runtime", analyticsData.analyticsDataRunData.runTime.ToString()},
        });

        Aptabase.TrackEvent("Main Menu Selections", new Dictionary<string, object>
        {
            {"Class Selected", analyticsData.analyticsDataRunData.classSelected},
            {"Difficulty Selected", analyticsData.analyticsDataRunData.difficultySelected}
        });

        Aptabase.TrackEvent("Beat The Run", new Dictionary<string, object>
        {
            {"Boss Killed", analyticsData.analyticsDataRunData.bossKilled}
        });

        //Assistants
        Dictionary<string, object> hiringBooth = new Dictionary<string, object>
        {
            {"Number Of Times Assistants Rerolled", analyticsData.analyticsDataRunData.numberOfAssistantsRerolled.ToString()},
            {"Number Of Assistants Fired", analyticsData.analyticsDataRunData.numberOfAssistantsFired.ToString()}
        };
        Aptabase.TrackEvent("Hiring Booth", hiringBooth);

        foreach (string assistant in analyticsData.analyticsDataRunData.assistantsChosen)
        {
            Dictionary<string, object> assistantChosen = new Dictionary<string, object>
            {
                {"Assistant Chosen", assistant}
            };
            Aptabase.TrackEvent("Assistant Chosen", assistantChosen);

            if (!applicationClose)
            {
                yield return cachedAnalytics;
            }
        }

        //Weapons
        Dictionary<string, object> weaponsShop = new Dictionary<string, object>
        {
            {"Number Of Times Weapons Rerolled", analyticsData.analyticsDataRunData.numberOfWeaponsRerolled.ToString()},
            {"Number Of Weapons Combined And Sold", analyticsData.analyticsDataRunData.numberOfWeaponsCombinedAndSold.ToString()}
        };
        Aptabase.TrackEvent("Weapons Shop", weaponsShop);

        foreach (string weapon in analyticsData.analyticsDataRunData.weaponsChosen)
        {
            Dictionary<string, object> weaponChosen = new Dictionary<string, object>
            {
                {"Weapon Chosen", weapon}
            };
            Aptabase.TrackEvent("Weapon Chosen", weaponChosen);

            if (!applicationClose)
            {
                yield return cachedAnalytics;
            }
        }

        //Wave Data
        Aptabase.TrackEvent("Number Of Waves Revealed", new Dictionary<string, object>
        {
            {"Reveal Amount", analyticsData.analyticsDataRunData.numberOfWavesRevealed.ToString()}
        });

        foreach (AnalyticsData.AnalyticsDataWaveData waveData in analyticsData.analyticsDataRunData.waveData)
        {
            string compiledString = "";
            foreach (string enemyGroup in waveData.enemyGroups)
            {
                compiledString += $"{enemyGroup},";
            }
            compiledString = compiledString.TrimEnd(','); 

            Dictionary<string, object> sortedWaveBreakdown = new Dictionary<string, object>
            {
            {"Wave Number", waveData.waveNumber.ToString()},
            {"Wave Type", waveData.waveType},
            {"Money Earned", waveData.moneyEarned.ToString()},
            {"Enemy Groups", compiledString}
            };
            Aptabase.TrackEvent("Wave Breakdown", sortedWaveBreakdown);

            if (!applicationClose)
            {
                yield return cachedAnalytics;
            }
        }

        Aptabase.Flush();
        Debug.LogWarning("Saving analytics file and sending analytics files to server");
    }
}