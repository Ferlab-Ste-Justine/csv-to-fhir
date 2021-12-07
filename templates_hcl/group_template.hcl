resource "keycloak_group" "$organization_id" {
  realm_id = keycloak_realm.clin.id
  name     = "$organization_name"
  attributes = {
    "fhir_organization_id" = "$organization_id"
  }
}

resource "keycloak_group_memberships" "group_members_$organization_id" {
  realm_id = keycloak_realm.clin.id
  group_id = keycloak_group.$organization_id.id

  members = [
    $members
  ]
}