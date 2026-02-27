/* * Alterações para Segurança e controle maior da execução (Versão 3.0)
 * * Propósito: Mover todas as credenciais sensíveis (Client ID, Secret Key, ID da Planilha)
 * do código-fonte (hardcoding) para um armazenamento seguro e externo.
 * As chaves agora são lidas do 'PropertiesService' (Propriedades do Script), o que
 * evita o risco de vazamento caso o código seja publicado (ex: no GitHub).
 * * Referência para validação e manutenção das chaves:
 * https://developers.google.com/apps-script/reference/properties?hl=pt-br
 *  * - Implementação de 'try...catch' e 'muteHttpExceptions: true' para garantir a 
 * resiliência e notificação por e-mail em caso de falha de renovação (400, 401, etc.).
 * - Correção do Escopo: Inicialização da Planilha e das Abas dentro da função, 
 * após a leitura segura do ID, evitando variáveis globais desnecessárias.
 */
// Declarações globais
const app = SpreadsheetApp;

function refresh_token() {
  // OBTENÇÃO SEGURA DE CREDENCIAIS E CONFIGURAÇÕES
  const props = PropertiesService.getScriptProperties().getProperties();
  // Nomes das chaves salvas no Propriedades do Script
  const CLIENT_ID = props.id_app; 
  const CLIENT_SECRET = props.secret_key;
  const SPREADSHEET_ID = props.table_id;
  
  const EMAIL_ALERTA = props.EMAIL_DE_ALERTA || Session.getActiveUser().getEmail();
  const URL_TOKEN = "https://api.mercadolibre.com/oauth/token"; 
  
  if (!CLIENT_ID || !CLIENT_SECRET || !SPREADSHEET_ID) {
    Logger.log("ERRO CRÍTICO: Credenciais ou SPREADSHEET_ID não encontrados no PropertiesService.");
    MailApp.sendEmail(EMAIL_ALERTA, " Falha na configuração de Segredos ML", "As chaves id_app, secret_key ou table_id estão faltando nas Propriedades do Script.");
    return; 
  }

  // INICIALIZAÇÃO DA PLANILHA DENTRO DA FUNÇÃO 
  const spreadsheet = app.openById(SPREADSHEET_ID); 
  const page_code = spreadsheet.getSheetByName('code'); 
  const page_access = spreadsheet.getSheetByName('access');
  
  // INÍCIO DO BLOCO RESILIENTE
  try {
    const refresh_token_antigo = page_code.getRange('B2').getValue(); // Pega valor do token na celular B2
    
    // Montagem do payload usando Template Literals
    const payload = `grant_type=refresh_token&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&refresh_token=${refresh_token_antigo}`;
    
    // Objeto de configuração da requisição HTTP
    const options = {
      "method": "post",
      "payload": payload,
      "headers": { 
        'Accept': 'application/json', 
        'Content-Type': 'application/x-www-form-urlencoded' 
      },
      "muteHttpExceptions": true 
    };

    //EXECUÇÃO E LOG
    const resposta = UrlFetchApp.fetch(URL_TOKEN, options);
    let retorno_json_texto = resposta.getContentText(); 
    page_code.getRange('E2').setValue(retorno_json_texto); // Log do retorno bruto

    //TRATAMENTO DA RESPOSTA
    if (resposta.getResponseCode() === 200) {
      // SUCESSO
      const json = JSON.parse(retorno_json_texto); 
      
      page_access.getRange('B2').setValue(json.access_token);
      page_code.getRange('B2').setValue(json.refresh_token); 
      
      const data = Utilities.formatDate(new Date(), "GMT-3", "dd/MM/yyyy");
      const hora = Utilities.formatDate(new Date(), "GMT-3", "HH:mm:ss");

      page_code.getRange('C2').setValue(data);
      page_code.getRange('D2').setValue(hora);
      
      Logger.log(`Token ML renovado com sucesso. Novo refresh_token salvo.`);

    } else {
      // FALHA HTTP + NOTIFICAÇÃO
      const erro_detalhe = `Falha HTTP ${resposta.getResponseCode()}. Resposta da API: ${retorno_json_texto}`;
      Logger.log("ERRO DE RENOVAÇÃO DE TOKEN: " + erro_detalhe);

      MailApp.sendEmail(
        EMAIL_ALERTA,
        `Falha de Refresh do Token ML (${resposta.getResponseCode()})`,
        `O script de refresh falhou. Detalhes: ${erro_detalhe}`
      );
    }
    
  } catch (e) {
    // 6. FALHA INESPERADA (Alerta!)
    const erro_message = `Erro de Script Inesperado: ${e.toString()}`;
    Logger.log(erro_message);
    
    MailApp.sendEmail(
      EMAIL_ALERTA,
      "Erro de Script Inesperado no Apps Script",
      `O script quebrou. Detalhes: ${erro_message}`
    );
  }
}