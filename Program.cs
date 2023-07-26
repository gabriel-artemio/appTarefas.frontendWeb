using Microsoft.EntityFrameworkCore;
using Pomelo.EntityFrameworkCore.MySql;
using WebASPCrud.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();


//builder.Services.AddDbContext<Contexto>(options => options.UseMySql(
//    "server=localhost;initial catalog=dbprojeto;uid=root;pwd=arlabs2022",
//    Microsoft.EntityFrameworkCore.ServerVersion.Parse("6.3.10-mysql")));

builder.Services.AddDbContext<Contexto>
    (options => options.UseMySql(
        "server=localhost;initial catalog=dbprojeto;uid=root;pwd=arlabs2022",
        Microsoft.EntityFrameworkCore.ServerVersion.Parse("6.3.10-mysql")));

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();