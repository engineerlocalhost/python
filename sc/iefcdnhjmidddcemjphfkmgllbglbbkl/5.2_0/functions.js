// functions.js bypass - dengan trigger Start Extraction

$(document).ready(function () {
    // Bypass Access Key
    $('#status').html('Start');
    $('#status').attr('data', 'bypass');
    $('#status').attr('data-path', 'bypass_path');
    $('#status').attr('data-path-key', 'paid');
    $('#akey1').html('✔ Subscription Bypassed').css('color', 'green');
    $('#akey').html('✔ No Expiry').css('color', 'green');
    $('#dlimit').html('Unlimited');

    // Enable semua tombol
    $('#changelinks, #restart, #Extract, #Stop, #Clear').prop('disabled', false);

    // Re-attach handler ke tombol Start Extraction
    $('#changelinks').on('click', function () {
        console.log('🚀 Start Extraction clicked');

        // Jalankan scraping jika fungsi tersedia
        if (typeof extractData === 'function') {
            extractData(); // Fungsi utama ekstraksi
        } else {
            console.log("⚠️ Fungsi 'extractData' tidak ditemukan. Pastikan script scraping terdefinisi.");
        }
    });
});

// Dummy placeholder (jika script utama tidak memuatnya)
function extractData() {
    alert("🔍 Data extraction logic belum dimasukkan.\nSilakan tambahkan fungsi `extractData()` sesuai kebutuhan.");
}
