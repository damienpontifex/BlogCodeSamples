using System;
using System.IO;
using System.Threading.Tasks;
using System.Threading;
using Microsoft.AspNetCore.Mvc;
using Azure.Identity;
using Azure.Storage.Blobs;

namespace app.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ValuesController : ControllerBase
    {
        private static Uri BlobUri = new Uri("https://tfazrolesstorageaccount.blob.core.windows.net/tf-az-roles-container/hello.txt");

        // GET api/values
        [HttpGet]
        public async Task<string> Get(CancellationToken cancellationToken)
        {
            var credential = new DefaultAzureCredential();
            var blob = new BlobClient(BlobUri, credential);
            var content = (await blob.DownloadAsync(cancellationToken)).Value.Content;

            using (var reader = new StreamReader(content))
            {
                var contents = await reader.ReadToEndAsync();
                return contents;
            }
        }
    }
}
