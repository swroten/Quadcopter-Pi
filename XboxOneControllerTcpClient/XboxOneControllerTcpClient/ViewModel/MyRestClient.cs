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
        // If connected directly: 192.168.10.1
        // If connected via same router and not directly: 10.0.0.104
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

        public async Task<Observed> Update(Observed observedData, Commanded commandedData)
        {
            return await UpdateFlightData(observedData, commandedData).ConfigureAwait(false);
        }

        private async Task<Observed> UpdateFlightData(Observed observedData, Commanded commandedData)
        {
            // Initialize Variables
            Observed observedDataServerResponse = observedData;
            Commanded commandedDataServerResponse = commandedData;

            try
            {
                // Get New Observed Flight Data from Server
                observedDataServerResponse = await GetObservedDataAsync($"/observed").ConfigureAwait(false);

                // Update Server with Commanded Flight Data
                commandedDataServerResponse = await UpdateFlightDataAsync(commandedData).ConfigureAwait(false);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }

            // return final response
            return observedDataServerResponse;
        }

        private async Task<Observed> GetObservedDataAsync(string path)
        {
            string flightDataAsString;
            Observed flightData = null;
            HttpResponseMessage response = await _client.GetAsync(path).ConfigureAwait(false);
            if (response.IsSuccessStatusCode)
            {
                // Get Flight Data as string
                flightDataAsString = await response.Content.ReadAsStringAsync().ConfigureAwait(false);

                // Deserialize
                flightData = JsonConvert.DeserializeObject<Observed>(flightDataAsString);
            }
            return flightData;
        }

        private async Task<Commanded> UpdateFlightDataAsync(Commanded commandedData)
        {
            string flightDataAsString;
            HttpResponseMessage response = await _client.PutAsJsonAsync($"/commands/{commandedData.Id}", commandedData).ConfigureAwait(false);
            response.EnsureSuccessStatusCode();

            // Get Flight Data as string
            flightDataAsString = await response.Content.ReadAsStringAsync().ConfigureAwait(false);

            // Deserialize
            commandedData = JsonConvert.DeserializeObject<Commanded>(flightDataAsString);

            // Return FlightData
            return commandedData;
        }
        
        private HttpClient _client;
    }
}
