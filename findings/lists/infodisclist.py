headers = [
    # This list only checks the header names, not their values. This could be changed later on, though should not be needed for information disclosures.
    #ToDo: add a short description to each and change it, such that this is also part of the text.
    "X-AspNet-Version",
    "X-AspNetMvc-Version",
    "Server",
    "X-Powered-By",
    "MicrosoftSharePointTeamServices"
]

body = {
    # Still buggy -.-
    # Key of the dictionary is the name of the information disclosure, that is going to be in the text.
    # Value of the dictionary is an array, which contains ALL the substrings that need to exists for it to be a finding.
    #"Keycloak": ["keycloak/auth/resources/", "/admin/keycloak"],
    #"Apache Tomcat": ["Apache Tomcat/"]
}
body["Keycloak"] = ["keycloak/auth/resources/", "/admin/keycloak"]
body["Apache Tomcat"] = ["Apache Tomcat/"]