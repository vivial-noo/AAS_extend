from basyx.aas import model
from basyx.aas.adapter.xml import write_aas_xml_file
############################################################################################
# Step 1: Create a Simple Asset Administration Shell Containing an AssetInformation object #
############################################################################################
# Step 1.1: create the AssetInformation object
asset_information = model.AssetInformation(
    asset_kind=model.AssetKind.INSTANCE,
    global_asset_id='http://acplt.org/Battery_Asset'
)

# step 1.2: create the Asset Administration Shell
identifier = 'https://acplt.org/Battery_AAS'
aas = model.AssetAdministrationShell(
    id_=identifier,  # set identifier
    asset_information=asset_information
)
#############################################################
# Step 2: Create a Simple Submodel Without SubmodelElements #
#############################################################

# Step 2.1: create the Submodel object
identifier = 'https://acplt.org/Passport_ID/did:web:acme.battery.pass:0226151e-949c-d067-8ef3-162431e28976'
submodel = model.Submodel(
    id_=identifier
)

# Step 2.2: create a reference to that Submodel and add it to the Asset Administration Shell's `submodel` set
aas.submodel.add(model.ModelReference.from_referable(submodel))

###############################################################
# Step 3: Create a Simple Property and Add it to the Submodel #
###############################################################

# Step 3.1: create a global reference to a semantic description of the Property
# A global reference consist of one key which points to the address where the semantic description is stored
semantic_reference_RawMaterialExtraction= model.ExternalReference(
    (model.Key(
        type_=model.KeyTypes.GLOBAL_REFERENCE,
        value='http://acplt.org/Properties/Battery_RawMaterialExtraction'
    ),)
)
semantic_reference_MainProduction = model.ExternalReference(
    (model.Key(
        type_=model.KeyTypes.GLOBAL_REFERENCE,
        value='http://acplt.org/Properties/Battery_MainProduction'
    ),)
)
semantic_reference_Distribution = model.ExternalReference(
    (model.Key(
        type_=model.KeyTypes.GLOBAL_REFERENCE,
        value='http://acplt.org/Properties/Battery_Distribution'
    ),)
)
semantic_reference_Recycling = model.ExternalReference(
    (model.Key(
        type_=model.KeyTypes.GLOBAL_REFERENCE,
        value='http://acplt.org/Properties/Battery_Recycling'
    ),)
)

# Step 3.2: create the simple Property
RawMaterialExtraction_ = model.Property(
    id_short='RawMaterialExtraction',  # Identifying string of the element within the Submodel namespace
    value_type=model.datatypes.Double,  # Data type of the value
    value=89.0,  # Value of the Property
    semantic_id=semantic_reference_RawMaterialExtraction  # set the semantic reference
)
MainProduction_ = model.Property(
    id_short='MainProduction',  # Identifying string of the element within the Submodel namespace
    value_type=model.datatypes.Double,  # Data type of the value
    value=30.0,  # Value of the Property
    semantic_id=semantic_reference_MainProduction # set the semantic reference
)
Distribution_ = model.Property(
    id_short='Distribution',  # Identifying string of the element within the Submodel namespace
    value_type=model.datatypes.Double,  # Data type of the value
    value=10.0,  # Value of the Property
    semantic_id=semantic_reference_Distribution  # set the semantic reference
)
Recycling_ = model.Property(
    id_short='Recycling',  # Identifying string of the element within the Submodel namespace
    value_type=model.datatypes.Double,  # Data type of the value
    value=8.0,  # Value of the Property
    semantic_id=semantic_reference_Recycling  # set the semantic reference
)
# Step 3.3: add the Property to the Submodel
submodel.submodel_element.add(RawMaterialExtraction_)
submodel.submodel_element.add(MainProduction_)
submodel.submodel_element.add(Distribution_)
submodel.submodel_element.add(Recycling_)


data: model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
data.add(submodel)
write_aas_xml_file(file='Simple_Submodel.xml', data=data)


