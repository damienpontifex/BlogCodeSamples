using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Services.AppAuthentication;
using Microsoft.WindowsAzure.Storage.Auth;
using Microsoft.WindowsAzure.Storage.Blob;

namespace app.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ValuesController : ControllerBase
    {
        private static Uri BlobUri = new Uri("https://tfazrolesstorageaccount.blob.core.windows.net/tf-az-roles-container/hello.txt");

        // GET api/values
        [HttpGet]
        public async Task<ActionResult<string>> Get()
        {
            var accessToken = await GetStorageAccessTokenAsync();
            var credential = new TokenCredential(accessToken);

            var storageCredentials = new StorageCredentials(credential);
            var blob = new CloudBlockBlob(BlobUri, storageCredentials);

            using (var reader = new StreamReader(await blob.OpenReadAsync()))
            {
                var contents = await reader.ReadToEndAsync();
                return contents;
            }
        }

        private Task<string> GetStorageAccessTokenAsync()
        {
            var azureServiceTokenProvider = new AzureServiceTokenProvider();
            return azureServiceTokenProvider.GetAccessTokenAsync(resource: "https://storage.azure.com/");
        }
    }
}
