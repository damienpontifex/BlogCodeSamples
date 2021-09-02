using Weather.Api;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Docker.DotNet;
using Docker.DotNet.Models;
using System.Collections.Generic;
using Microsoft.Extensions.Configuration;
using System;

namespace Weather.Api.Tests
{
    public class ListsApiWebApplicationFactory : WebApplicationFactory<Startup>
    {
        const string DB_PASSWORD = "p@ssw0rd";
        private readonly ContainerManager _containerManager = new ContainerManager();

        private readonly Random _random = new Random();
        private readonly bool IsCi = !string.IsNullOrEmpty(Environment.GetEnvironmentVariable("TF_BUILD"));

        protected override void ConfigureWebHost(IWebHostBuilder builder)
        {
            var port = IsCi ? "17875" : _random.Next(10_000, 20_000).ToString();

            if (!IsCi)
            {
                _containerManager.StartContainerAsync("mcr.microsoft.com/mssql/server:2017-latest", new List<string>
                {
                    "ACCEPT_EULA=Y",
                    $"SA_PASSWORD={DB_PASSWORD}"
                }, ("1433", port)).GetAwaiter().GetResult();
            }

            base.ConfigureWebHost(builder);

            builder.ConfigureAppConfiguration((context, config) =>
            {
                config.AddInMemoryCollection(new Dictionary<string, string>
                {
                    ["ConnectionStrings:Default"] = $"data source=localhost,{port};initial catalog=WeatherDb;User=sa;Password={DB_PASSWORD};multipleactiveresultsets=True;"
                });
            });

            builder.ConfigureServices(services =>
            {
                var sp = services.BuildServiceProvider();
                using (var scope = sp.CreateScope())
                {
                    var db = scope.ServiceProvider.GetRequiredService<ListDbContext>();
                    db.Database.Migrate();
                }
            });
        }

        protected override void Dispose(bool disposing)
        {
            _containerManager.Dispose();

            base.Dispose(disposing);
        }
    }
}
