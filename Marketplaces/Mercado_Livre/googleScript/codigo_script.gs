// Esse é um código de exemplo, você pode usar para automatizar seu script no Google

let app = SpreadsheetApp;
let spreeadsheet = app.openById('ID_DA_SUA_PLANILHA_AQUI');

let page_code = spreeadsheet.getSheetByName('code');
let page_access = spreeadsheet.getSheetByName('access');

var code = page_code.getRange('B2');

var id_app = 'ID_DO_SEU_APP_AQUI'
var secret_key = 'CHAVE_SECRETA_AQUI'

function refresh_token() {
  var code_antigo = page_code.getRange('C2').getValue();
  page_code.getRange('B2').setValue(code_antigo);

  var url = "https://api.mercadolibre.com/oauth/token"
  var payload = 'grant_type=refresh_token&client_id=' + id_app + '&client_secret=' + secret_key + '&refresh_token=' + code_antigo;
  var options = {
    "method": "post",
    "payload": payload,
    "headers": {
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  };

  var resposta = UrlFetchApp.fetch(url, options);
  retorno = resposta.getContentText()

  page_code.getRange('F2').setValue(retorno)

  var json = JSON.parse(resposta.getContentText());
  page_access.getRange('B2').setValue(json.access_token);
  page_code.getRange('C2').setValue(json.refresh_token);

  var data = Utilities.formatDate(new Date(), "GMT-3", "dd/MM/yyyy");
  var hora = Utilities.formatDate(new Date(), "GMT-3", "HH:mm:ss");

  page_code.getRange('D2').setValue(data);
  page_code.getRange('E2').setValue(hora);


}