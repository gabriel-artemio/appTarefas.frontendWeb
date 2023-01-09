using Microsoft.AspNetCore.Mvc;

namespace CoreMVC_SistemaProdutos.Controllers
{
    public class ProdutoController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        public IActionResult InserirProduto()
        {
            return View();
        }

        public IActionResult EditarProduto()
        {
            return View();
        }

        public IActionResult ApagarConfirmacao()
        {
            return View();
        }
    }
}