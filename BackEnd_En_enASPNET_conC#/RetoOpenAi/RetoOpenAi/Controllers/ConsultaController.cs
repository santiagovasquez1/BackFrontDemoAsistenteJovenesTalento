using System;
using System.Threading.Tasks;
using System.Web.Http;
using RetoOpenAI.Clases;

namespace RetoOpenAI.Controllers
{
    [RoutePrefix("api/consulta")]
    public class ConsultaController : ApiController
    {
        private static ManejadorConsultas manejadorConsulta = new ManejadorConsultas();
        //private ManejadorConsultas manejadorConsulta = new ManejadorConsultas();

        [HttpPost]
        [Route("consultar")]
        public async Task<IHttpActionResult> Consultar([FromBody] ConsultaRequest request)
        {
            if (request == null || string.IsNullOrEmpty(request.Pregunta))
            {
                return BadRequest("No se proporcionó ninguna pregunta.");
            }

            try
            {
                var response = await manejadorConsulta.MostrarConsulta(request.Pregunta);
                return ResponseMessage(response);
            }
            catch (Exception ex)
            {
                return InternalServerError(ex);
            }
        }
    }

    public class ConsultaRequest
    {
        public string Pregunta { get; set; }
    }
}