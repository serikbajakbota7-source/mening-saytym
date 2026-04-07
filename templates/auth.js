// auth.js - Supabase конфигурациясы
// Бұл файлды барлық HTML беттеріне қосу керек

const SUPABASE_URL = 'https://СЕНІҢ-ПРОЕКТ-URL.supabase.co';
const SUPABASE_ANON_KEY = 'СЕНІҢ-ANON-KEY';

// Supabase клиентін инициализациялау
let supabaseClient = null;

document.addEventListener('DOMContentLoaded', function() {
    if (typeof supabase !== 'undefined') {
        supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        console.log('Supabase қосылды');
    } else {
        console.error('Supabase кітапханасы жүктелмеген');
    }
});

// Пайдаланушы сессиясын тексеру
async function checkAuth() {
    if (!supabaseClient) return null;
    const { data: { session }, error } = await supabaseClient.auth.getSession();
    return session;
}

// Шығу функциясы
async function logout() {
    if (!supabaseClient) return;
    await supabaseClient.auth.signOut();
    localStorage.clear();
    window.location.href = 'register.html';
}
