using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Docker.DotNet;
using Docker.DotNet.Models;

namespace Weather.Api.Tests
{
    public class ContainerManager : IDisposable
    {
        private readonly DockerClient _dockerClient;
        private List<CreateContainerResponse> _containers = new List<CreateContainerResponse>();

        public ContainerManager()
        {
            var dockerUri = Environment.OSVersion.Platform == PlatformID.Win32NT ? "npipe://./pipe/docker_engine" : "unix:///var/run/docker.sock";

            _dockerClient = new DockerClientConfiguration(new Uri(dockerUri)).CreateClient();
        }

        public async Task StartContainerAsync(string image, List<string> env, (string containerPort, string localPort) ports)
        {
            var containerOptions = new CreateContainerParameters
            {
                Image = image,
                Env = env,
                HostConfig = new HostConfig
                {
                    PortBindings = new Dictionary<string, IList<PortBinding>>
                        {
                            { $"{ports.containerPort}/tcp", new List<PortBinding> { new PortBinding { HostPort = ports.localPort } } }
                        }
                }
            };
            var container = await _dockerClient.Containers.CreateContainerAsync(containerOptions);
            await _dockerClient.Containers.StartContainerAsync(container.ID, new ContainerStartParameters());
            _containers.Add(container);
        }

        public void Dispose()
        {
            foreach (var container in _containers)
            {
                _dockerClient.Containers.StopContainerAsync(container.ID, new ContainerStopParameters()).GetAwaiter().GetResult();
                _dockerClient.Containers.RemoveContainerAsync(container.ID, new ContainerRemoveParameters()).GetAwaiter().GetResult();
            }
        }
    }
}
