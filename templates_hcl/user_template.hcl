resource "keycloak_user" "$practitioner_id" {
  realm_id = keycloak_realm.clin.id
  username = "$username"
  enabled  = true

  email      = "$email"
  first_name = "$first_name"
  last_name  = "$last_name"
  email_verified = true

  attributes = {
    "fhir_practitioner_id" = "$practitioner_id"
    "locale" = "fr"
  }

  initial_password {
    value = "$password"
    temporary = false
  }
}

resource "keycloak_user_roles" "$practitioner_id_roles" {
  realm_id = keycloak_realm.clin.id
  user_id  = keycloak_user.$practitioner_id.id

  role_ids = [
    $roles
  ]
}