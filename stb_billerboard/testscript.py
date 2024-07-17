import requests
import json

url = "https://api.lexoffice.io/v1/invoices"

payload = json.dumps({
  "id": None,
  "organizationId": None,
  "createdDate": None,
  "updatedDate": None,
  "version": None,
  "archived": False,
  "voucherStatus": None,
  "voucherNumber": None,
  "voucherDate": "2024-03-06T00:00:00.000+02:00",
  "dueDate": None,
  "address": {
    "contactId": None,
    "name": "Api Testunternehmen",
    "street": "Musterstraße 42",
    "city": "Hennigsdorf",
    "zip": "16761",
    "countryCode": "DE"
  },
  "lineItems": [
    {
      "id": None,
      "type": "custom",
      "name": "Lizenznutzung",
      "description": "Tools: Xing Talentmanager, Hubspot, Aircall, Index, Data Entry, Office 365, Join, Pallas",
      "quantity": 3,
      "unitName": "Monate",
      "unitPrice": {
        "currency": "EUR",
        "netAmount": 466.70,
        #"grossAmount": 15.95,
        "taxRatePercentage": 19
      },
      #"discountPercentage": 50,
      #"lineItemAmount": 13.4
    },
    {
      "type": "text",
      "name": "Strukturieren Sie Ihre Belege durch Text-Elemente.",
      "description": "Das hilft beim Verständnis"
    }
  ],
  "totalPrice": {
    "currency": "EUR",
    #"totalNetAmount": 26.72,
    #"totalGrossAmount": 29.85,
    #"taxRatePercentage": None,
    #"totalTaxAmount": 3.13,
    #"totalDiscountAbsolute": None,
    #"totalDiscountPercentage": None
  },
#  "taxAmounts": [
#    {
#      "taxRatePercentage": 19,
#      "taxAmount": 2.55,
#      "amount": 15.95
#    }
#  ],
  "taxConditions": {
    "taxType": "net",
    "taxTypeNote": None
  },
  #"paymentConditions": {
  #  "paymentTermLabel": "10 Tage - 3 %, 30 Tage netto",
  #  "paymentTermDuration": 30,
  #  "paymentDiscountConditions": {
  #    "discountPercentage": 3,
  #    "discountRange": 10
  #  }
  #},
  "shippingConditions": {
    "shippingDate": "2023-07-03T00:00:00.000+02:00",
    "shippingEndDate": None,
    "shippingType": "delivery"
  },
  "title": "Rechnung",
  "introduction": "Unsere Lieferungen/Leistungen stellen wir Ihnen wie folgt in Rechnung.",
  "remark": """Diese Rechnung wurde im Factoringverfahren an die Wolf Factoring, Robert Wolf GmbH, Esslinger Str. 7, 70771 LE-Echterdingen, übertragen. Eine Zahlung kann somit nur an diese mit schuldbefreiender Wirkung erfolgen. Bitte bezahlen Sie an Kontoinhaber:
Robert Wolf GmbH, KSK Esslingen,
IBAN-Code: DE40 6115 0020 0100 666306; BIC-Code: ESSLDE66XXX

Vielen Dank für die gute Zusammenarbeit."""
})
headers = {
  'Authorization': 'Bearer _hTkaSsxsM1-MgUhsq7bJU7wxPQ2JkyNxvJfwmcMJpBcq9iw',
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
