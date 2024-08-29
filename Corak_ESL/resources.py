from import_export import resources
from import_export.fields import Field
from .models import Export2Zkong
import logging

logger = logging.getLogger('corak_esl')


class Export2ZkongResource(resources.ModelResource):
    store_profile = Field(attribute='store_profile', column_name='Store Profile')
    barCode = Field(attribute='barCode', column_name='Bar Code')
    updated_at = Field(attribute='updated_at', column_name='Updated At')
    custFeature50 = Field(attribute='custFeature50', column_name='Cust Feature 50')
    attrCategory = Field(attribute='attrCategory', column_name='Attr Category')
    attrName = Field(attribute='attrName', column_name='Attr Name')
    productCode = Field(attribute='productCode', column_name='Product Code')
    productSku = Field(attribute='productSku', column_name='Product SKU')
    itemTitle = Field(attribute='itemTitle', column_name='Item Title')
    shortTitle = Field(attribute='shortTitle', column_name='Short Title')
    classLevel = Field(attribute='classLevel', column_name='Class Level')
    productArea = Field(attribute='productArea', column_name='Product Area')
    unit = Field(attribute='unit', column_name='Unit')
    qrCode = Field(attribute='qrCode', column_name='QR Code')
    nfcUrl = Field(attribute='nfcUrl', column_name='NFC URL')
    spec = Field(attribute='spec', column_name='Spec')
    originalPrice = Field(attribute='originalPrice', column_name='Original Price')
    price = Field(attribute='price', column_name='Price')
    memberPrice = Field(attribute='memberPrice', column_name='Member Price')
    stock1 = Field(attribute='stock1', column_name='Stock 1')
    stock2 = Field(attribute='stock2', column_name='Stock 2')
    stock3 = Field(attribute='stock3', column_name='Stock 3')
    proStartTime = Field(attribute='proStartTime', column_name='Promotion Start Time')
    proEndTime = Field(attribute='proEndTime', column_name='Promotion End Time')
    promotionText = Field(attribute='promotionText', column_name='Promotion Text')
    custFeature1 = Field(attribute='custFeature1', column_name='Cust Feature 1')
    custFeature2 = Field(attribute='custFeature2', column_name='Cust Feature 2')
    custFeature3 = Field(attribute='custFeature3', column_name='Cust Feature 3')

    class Meta:
        model = Export2Zkong
        fields = (
            'store_profile', 'barCode', 'updated_at', 'custFeature50', 'attrCategory', 'attrName', 
            'productCode', 'productSku', 'itemTitle', 'shortTitle', 'classLevel', 'productArea', 
            'unit', 'qrCode', 'nfcUrl', 'spec', 'originalPrice', 'price', 'memberPrice', 'stock1', 
            'stock2', 'stock3', 'proStartTime', 'proEndTime', 'promotionText', 'custFeature1', 
            'custFeature2', 'custFeature3'
        )
        export_order = fields
