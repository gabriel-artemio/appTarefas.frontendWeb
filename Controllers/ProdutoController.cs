using Microsoft.AspNetCore.Mvc;

namespace CoreMVC_SistemaProdutos.Controllers
{
    public class ProdutoController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}