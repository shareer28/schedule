import duckdb
from app.models.organizations import Organizations, Organization
def get_organizations() -> Organizations:
    conn = duckdb.connect(":memory:")
    organizations = [
        Organization(id = r[1],name=r[0] )
        for r in conn.read_csv("./data/organization.csv").fetchall()
    ]
    conn.close()
    query_result = Organizations(organizations=organizations)
    return query_result

def get_organization(id : str) -> Organization:
    conn = duckdb.connect(":memory:")
    organization = conn.read_csv("./data/organization.csv").filter(f"organisation_id = '{id}'").fetchone()
    if not organization: 
        return None
    
    return Organization(id=organization[1], name=organization[0])

    