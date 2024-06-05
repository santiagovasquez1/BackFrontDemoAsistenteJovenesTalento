using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using System.Web.Http;
using static System.Net.WebRequestMethods;

namespace RetoOpenAI.Clases
{
    public class ManejadorConsultas
    {
        // Se declaran variables para almacenar configuraciones esenciales para la interacción
        // con la API de OpenAI de una manera centralizada y fácilmente configurable.

        private readonly string apiKey = ConfigurationManager.AppSettings["AZURE_OPENAI_API_KEY"];
        private readonly string apiEndpoint = ConfigurationManager.AppSettings["AZURE_OPENAI_API_ENDPOINT"];
        private readonly string assistantModel = ConfigurationManager.AppSettings["AZURE_OPENAI_API_MODEL"];
        private readonly string versionApi = ConfigurationManager.AppSettings["AZURE_OPENAI_API_VERSION"];

        private List<Tuple<string, string>> contexto = new List<Tuple<string, string>>();

        // constructor
        public ManejadorConsultas() { }

        //Método para enviar pregunta y recibir una respuesta
        public async Task<HttpResponseMessage> MostrarConsulta(string pregunta)
        {
            try
            {
                if (string.IsNullOrEmpty(apiKey) || string.IsNullOrEmpty(apiEndpoint))
                {
                    throw new Exception("AZURE_OPENAI_API_KEY o AZURE_OPENAI_API_ENDPOINT no están configurados correctamente.");
                }

                string url = $"{apiEndpoint}/deployments/{assistantModel}/chat/completions?api-version={versionApi}";

                using (var client = new HttpClient())
                {
                    client.DefaultRequestHeaders.Add("api-key", apiKey);

                    //  objeto anónimo
                    //  la información necesaria
                    //  para enviar una solicitud a la API de OpenAI.
                    var data = new
                    {
                        messages = contexto.Select(t => new { role = "user", content = t.Item1 }).Append(new { role = "user", content = pregunta }),
                        temperature = 0.5,
                        max_tokens = 1000,
                        top_p = 1,
                        frequency_penalty = 0,
                        presence_penalty = 0
                    };
                    // se convierte el objeto data a JSON
                    // Envía una solicitud HTTP POST a la URL especificada con el JSON en el cuerpo de la solicitud.
                    // Espera asincrónicamente la respuesta del servidor.
                    // Almacena la respuesta en la variable response.

                    var response = await client.PostAsJsonAsync(url, data);

                    if (response.IsSuccessStatusCode)   //  Verifica si el código de estado HTTP
                                                        //  de la respuesta indica éxito (códigos de estado en el rango 200-299).
                                                        // Procesamiento de la Respuesta en Caso de
                    {
                        // Se lee el contenido de la respuesta HTTP
                        // y lo deserializa en un objeto dinámico(dynamic),
                        // lo que permite acceder a las propiedades del JSON recibido
                        // sin necesidad de definir una estructura de datos específica.

                       var responseData = await response.Content.ReadAsAsync<dynamic>();


                        JObject jsonObject = new JObject();
                        string respuesta = responseData.choices[0].message.content;
                        jsonObject["respuesta"] = respuesta;
                        
                        // Se guarda el historial
                        contexto.Add(new Tuple<string, string>(pregunta, respuesta));

                        return new HttpResponseMessage(HttpStatusCode.OK)
                        {
                            //Content = new StringContent("{\"respuesta\": \"" + respuesta + "\"}")
                            Content = new StringContent(jsonObject.ToString())
                        };
                    }
                    else
                    {
                        return new HttpResponseMessage(HttpStatusCode.InternalServerError)
                        {
                            Content = new StringContent("{\"error\": \"" + $"Error al generar mensaje: {response.ReasonPhrase}" + "\"}")
                        };
                    }
                }
            }
            catch (Exception ex)
            {
                return new HttpResponseMessage(HttpStatusCode.InternalServerError)
                {
                    Content = new StringContent("{\"error\": \"" + $"Ocurrió un error: {ex.Message}" + "\"}")
                };
            }
        }
    }
}