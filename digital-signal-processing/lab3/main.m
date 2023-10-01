% n = 2, R_p = 3, R_s = 45, Фильтр высоких частот, режекторный

n = 2;
Rp = 3;
Rs = 45;
w = 0:0.1:5;                    

%% Фильтр Баттерворта - АЧХ
[z, p, k] = buttap(n);		
[b, a] = zp2tf(z, p, k);				
h = freqs(b, a, w);
plot(w, abs(h));
sgtitle("Фильтр Баттерворта");
%% Фильтр Чебышёва первого рода - АЧХ
[z, p, k] = cheb1ap(n, Rp);		
[b, a] = zp2tf(z, p, k);				
h = freqs(b, a, w);
plot(w, abs(h));
sgtitle("Фильтр Чебышёва первого рода");
%% Фильтр Чебышёва второго рода - АЧХ
[z, p, k] = cheb2ap(n, Rs);     
[b, a] = zp2tf(z, p, k);                     
h = freqs(b, a, w);
plot(w, abs(h));   
sgtitle("Фильтр Чебышёва второго рода");
%% Эллиптический фильтр - АЧХ
[z, p, k] = ellipap(n, Rp, Rs);     
[b, a] = zp2tf(z, p, k);                     
h = freqs(b, a, w);
plot(w, abs(h));
sgtitle("Эллиптический фильтр");
%% Фильтр Бесселя - АЧХ
[z, p, k] = besselap(n);        
[b, a] = zp2tf(z, p, k);                    
h = freqs(b, a, w);
plot(w, abs(h));
sgtitle("Фильтр Бесселя");
%% Фильтр Баттерворта
[z, p, k] = buttap(n);		
[b, a] = zp2tf(z, p, k);				
h = freqs(b, a, w);
subplot(1, 3, 1);
plot(w, abs(h));
legend("АЧХ");

w0 = 3;                
[b1, a1] = lp2hp(b, a, w0);
h = freqs(b1, a1, w);
subplot(1, 3, 2);
plot(w, abs(h));
legend("ФВЧ");

w1 = 2;
w2 = 4;
w0 = sqrt(w1 * w2);
Q = w0/(w2 - w1);
[b1, a1] = lp2bs(b, a, w0, Q);
h = freqs(b1, a1, w);
subplot(1, 3, 3);
plot(w, abs(h));
legend("Режекторный");

sgtitle("Фильтр Баттерворта");
%% Фильтр Чебышёва первого рода
[z, p, k] = cheb1ap(n, Rp);		
[b, a] = zp2tf(z, p, k);				
h = freqs(b, a, w);
subplot(1, 3, 1);
plot(w, abs(h));

w0 = 3;                
[b1, a1] = lp2hp(b, a, w0);
h = freqs(b1, a1, w);
subplot(1, 3, 2);
plot(w, abs(h));
legend("ФВЧ");

w1 = 2;
w2 = 4;
w0 = sqrt(w1 * w2);
Q = w0/(w2 - w1);
[b1, a1] = lp2bs(b, a, w0, Q);
h = freqs(b1, a1, w);
subplot(1, 3, 3);
plot(w, abs(h));
legend("Режекторный");

sgtitle("Фильтр Чебышёва первого рода");

%% Фильтр Чебышёва второго рода
[z, p, k] = cheb2ap(n, Rs);     
[b, a] = zp2tf(z, p, k);                     
h = freqs(b, a, w);
subplot(1, 3, 1);
plot(w, abs(h));

w0 = 3;                
[b1, a1] = lp2hp(b, a, w0);
h = freqs(b1, a1, w);
subplot(1, 3, 2);
plot(w, abs(h));
legend("ФВЧ");

w1 = 2;
w2 = 4;
w0 = sqrt(w1 * w2);
Q = w0/(w2 - w1);
[b1, a1] = lp2bs(b, a, w0, Q);
h = freqs(b1, a1, w);
subplot(1, 3, 3);
plot(w, abs(h));
legend("Режекторный");

sgtitle("Фильтр Чебышёва второго рода");

%% Эллиптический фильтр
[z, p, k] = ellipap(n, Rp, Rs);     
[b, a] = zp2tf(z, p, k);                     
h = freqs(b, a, w);
subplot(1, 3, 1);
plot(w, abs(h));

w0 = 3;                
[b1, a1] = lp2hp(b, a, w0);
h = freqs(b1, a1, w);
subplot(1, 3, 2);
plot(w, abs(h));
legend("ФВЧ");

w1 = 2;
w2 = 4;
w0 = sqrt(w1 * w2);
Q = w0/(w2 - w1);
[b1, a1] = lp2bs(b, a, w0, Q);
h = freqs(b1, a1, w);
subplot(1, 3, 3);
plot(w, abs(h));
legend("Режекторный");

sgtitle("Эллиптический фильтр");
%% Фильтр Бесселя
[z, p, k] = besselap(n);  
[b, a] = zp2tf(z, p, k);                     
h = freqs(b, a, w);
subplot(1, 3, 1);
plot(w, abs(h));

w0 = 3;                
[b1, a1] = lp2hp(b, a, w0);
h = freqs(b1, a1, w);
subplot(1, 3, 2);
plot(w, abs(h));
legend("ФВЧ");

w1 = 2;
w2 = 4;
w0 = sqrt(w1 * w2);
Q = w0/(w2 - w1);
[b1, a1] = lp2bs(b, a, w0, Q);
h = freqs(b1, a1, w);
subplot(1, 3, 3);
plot(w, abs(h));
legend("Режекторный");

sgtitle("Фильтр Бесселя");