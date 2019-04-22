variable "app_name" {
  type        = "string"
  description = "The common name to use for resources"
  default     = "tf-az-roles"
}

variable "environment" {
  type        = "string"
  description = "The deployment environment description"
  default     = "dev"
}

resource "azurerm_resource_group" "test" {
  name     = "${var.app_name}-rg"
  location = "Australia East"

  tags = {
    environment = "${var.environment}"
  }
}
/* 
 * App Service
 */
resource "azurerm_app_service_plan" "test" {
  name                = "${var.app_name}-appserviceplan"
  location            = "${azurerm_resource_group.test.location}"
  resource_group_name = "${azurerm_resource_group.test.name}"

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "test" {
  name                = "${var.app_name}-app-service"
  location            = "${azurerm_resource_group.test.location}"
  resource_group_name = "${azurerm_resource_group.test.name}"
  app_service_plan_id = "${azurerm_app_service_plan.test.id}"

  identity {
    type = "SystemAssigned"
  }
}

/*
 * Storage
 */
resource "azurerm_storage_account" "test" {
  name                     = "${replace(var.app_name, "-", "")}storageaccount"
  resource_group_name      = "${azurerm_resource_group.test.name}"
  location                 = "${azurerm_resource_group.test.location}"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "test" {
  name                 = "${var.app_name}-container"
  storage_account_name = "${azurerm_storage_account.test.name}"
  resource_group_name  = "${azurerm_resource_group.test.name}"
}

resource "azurerm_storage_blob" "test" {
  name                   = "hello.txt"
  resource_group_name    = "${azurerm_resource_group.test.name}"
  storage_account_name   = "${azurerm_storage_account.test.name}"
  storage_container_name = "${azurerm_storage_container.test.name}"
  type                   = "block"
  content_type           = "application/text"
  source                 = "hello.txt"
}

/*
 * Roles and assignments
 */
// https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-reader
resource "azurerm_role_assignment" "test" {
  role_definition_name = "Storage Blob Data Reader"
  scope                = "${azurerm_storage_account.test.id}"
  principal_id         = "${azurerm_app_service.test.identity.0.principal_id}"
}
