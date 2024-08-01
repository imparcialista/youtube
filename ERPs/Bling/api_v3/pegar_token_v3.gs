const LOG_CODE = "code_bling";
const BLING_ACCESS = "conta_bling";
const SPREADSHEET_ID = "ID_DA_PLANILHA";
const BLING_API_URL = "https://www.bling.com.br/Api/v3/oauth/token";
const BASIC_AUTH = "Basic ENCODE_BASE_64";

let app = SpreadsheetApp;
let spreadsheet = app.openById(SPREADSHEET_ID);

let log_code_sheet = spreadsheet.getSheetByName(LOG_CODE);
let blingAccess = spreadsheet.getSheetByName(BLING_ACCESS);

function refreshToken() {
    try {
        const refreshToken = getRefreshToken();
        const response = fetchNewAccessToken(refreshToken);
        const json = parseResponse(response);
        updateSheets(json);
        logRefreshTime();
    } catch (error) {
        handleError(error);
    }
}

function getRefreshToken() {
    const code = log_code_sheet.getRange("C2").getValue();
    log_code_sheet.getRange("B2").setValue(code);
    return code;
}

function fetchNewAccessToken(refreshToken) {
    const payload = `grant_type=refresh_token&refresh_token=${refreshToken}`;
    const options = {
        method: "post",
        payload: payload,
        headers: {
            Accept: "1.0",
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: BASIC_AUTH,
        },
    };
    return UrlFetchApp.fetch(BLING_API_URL, options);
}

function parseResponse(response) {
    const responseText = response.getContentText();
    log_code_sheet.getRange("F2").setValue(responseText);
    return JSON.parse(responseText);
}

function updateSheets(json) {
    blingAccess.getRange("B2").setValue(json.access_token);
    log_code_sheet.getRange("C2").setValue(json.refresh_token);
}

function logRefreshTime() {
    const data = Utilities.formatDate(new Date(), "GMT-3", "dd/MM/yyyy");
    const hora = Utilities.formatDate(new Date(), "GMT-3", "HH:mm:ss");
    log_code_sheet.getRange("D2").setValue(data);
    log_code_sheet.getRange("E2").setValue(hora);
}

function handleError(error) {
    console.error("Error refreshing token:", error);
}
