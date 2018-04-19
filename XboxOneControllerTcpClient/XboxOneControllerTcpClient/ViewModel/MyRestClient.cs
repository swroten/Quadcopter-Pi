using Newtonsoft.Json;
using System;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using XboxOneControllerTcpClient.Model;

namespace XboxOneControllerTcpClient.ViewModel
{
    public class MyRestClient
    {
        public MyRestClient(string endpointUri = "http://10.0.0.104:5000/")
        {
            _client = new HttpClient
            {                
                // Update port # in the following line.
                BaseAddress = new Uri(endpointUri)
            };
            _client.DefaultRequestHeaders.Accept.Clear();
            _client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", 
                Convert.ToBase64String(Encoding.ASCII.GetBytes("pi:raspberry")));
        }

        public async Task<FlightData> Update(FlightData flightData)
        {
            return await UpdateFlightData(flightData).ConfigureAwait(false);
        }

        private async Task<FlightData> UpdateFlightData(FlightData flightData)
        {
            // Set to itself for initialization
            FlightData newFlightData;
            FlightData responseFlightData = flightData;

            try
            {
                // Get New Flight Data from Server
                newFlightData = await GetFlightDataAsync($"/flightdata").ConfigureAwait(false);

                // Update Current Flight Data
                flightData.ObservedYaw = newFlightData.ObservedYaw;
                flightData.ObservedRoll = newFlightData.ObservedRoll;
                flightData.ObservedPitch = newFlightData.ObservedPitch;
                flightData.ObservedThrottle = newFlightData.ObservedThrottle;

                // Display Flight Data on console for debugging
                ShowFlightData(flightData);

                // Update Server Flight Data with Demanded Values
                //responseFlightData = await UpdateFlightDataAsync(flightData).ConfigureAwait(false);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }

            // return final response
            return responseFlightData;
        }

        private async Task<FlightData> GetFlightDataAsync(string path)
        {
            string flightDataAsString;
            FlightData flightData = null;
            HttpResponseMessage response = await _client.GetAsync(path).ConfigureAwait(false);
            if (response.IsSuccessStatusCode)
            {
                // Get Flight Data as string
                flightDataAsString = await response.Content.ReadAsStringAsync().ConfigureAwait(false);

                // Deserialize
                flightData = JsonConvert.DeserializeObject<FlightData>(flightDataAsString);
            }
            return flightData;
        }

        private async Task<FlightData> UpdateFlightDataAsync(FlightData flightData)
        {
            string flightDataAsString;
            HttpResponseMessage response = await _client.PutAsJsonAsync($"/flightdata", flightData).ConfigureAwait(false);
            response.EnsureSuccessStatusCode();

            // Get Flight Data as string
            flightDataAsString = await response.Content.ReadAsStringAsync().ConfigureAwait(false);

            // Deserialize
            flightData = JsonConvert.DeserializeObject<FlightData>(flightDataAsString);

            // Return FlightData
            return flightData;
        }

        private void ShowFlightData(FlightData flightData)
        {
            Console.WriteLine(JsonConvert.SerializeObject(flightData, Formatting.Indented));
        }


        private HttpClient _client;
    }
}
