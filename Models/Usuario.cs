using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace WebASPCrud.Models
{
    [Table("usuario")]
    public class Usuario
    {
        [Display(Name = "Cód")]
        [Column("id")]
        public int Id { get; set; }

        [Display(Name = "Nome")]
        [Column("nome")]
        public string Nome { get; set; }
    }
}