amp = 0.1;
sr = 1000;
step = 1/sr;
t = (0:step:0.25);

freq1 = 20;
freq2 = 50;
freq3 = 60;

s1 = amp*sin(2*pi*freq1*t);
s2 = amp*sin(2*pi*freq2*t);
s3 = amp*sin(2*pi*freq3*t);

%% Фильтр Баттерворта, s1 + s2
s = s1 + s2;

subplot(4, 1, 1)
plot(t, s);
legend("s");

n = 4;
[z, p, k] = buttap(n);      
[b, a] = zp2tf(z, p, k);

w0 = 0.1;
[b1, a1] = lp2lp(b, a, w0);               
f = abs(filter(b1, a1, t));
sf = s1.*f + s2;

subplot(4, 1, 2);
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");


%% Фильтр Чебышева 1 рода, s1 + s2
s = s1 + s2;

subplot(4, 1, 1);
plot(t, s);
legend("s");

n = 4;
Rp = 0.1;
[z, p, k] = cheb1ap(n, Rp);
[b, a] = zp2tf(z, p, k);
w0 = 0.1;
[b1, a1] = lp2lp(b, a, w0);
             
f = abs(filter(b1, a1, t));
sf = s1.*f + s2;
subplot(4, 1, 2);
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");

%% Фильтр Чебышева 2 рода, s1 + s2
s = s1 + s2;

subplot(4, 1, 1);
plot(t, s);
legend("s");

n = 4;
Rs = 45;
w0 = 0.2;
[z, p, k] = cheb2ap(n, Rs);
[b, a] = zp2tf(z, p, k);

[b1, a1] = lp2hp(b, a, w0);
f = abs(filter(b1, a1, t));
sf = s1 + s2.*f;
subplot(4, 1, 2)
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");

%% Эллиптический фильтр, s1 + s2
s = s1 + s2;

subplot(4, 1, 1);
plot(t, s);
legend("s");

n = 4;
Rp = 0.1;
Rs = 45;
w1 = 0.05;
w2 = 0.15;
[z, p, k] = ellipap(n, Rp, Rs);
[b, a] = zp2tf(z, p, k);

w0 = sqrt(w1 * w2);
Bw = w2 - w1;
[b1, a1] = lp2bp(b, a, w0, Bw);
f = abs(filter(b1, a1, t));
sf = s1 + s2.*f;
subplot(4, 1, 2)
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");

%% Фильтр Баттерворта, s1 + s2 + s3
s = s1 + s2 + s3;

subplot(4, 1, 1);
plot(t, s);
legend("s");

n = 4;
[z, p, k] = buttap(n);
[b, a] = zp2tf(z, p, k);

w0 = 0.15;
[b1, a1] = lp2hp(b, a, w0);    
f = abs(filter(b1, a1, t));
sf = s1 + s2.*f + s3.*f;
subplot(4, 1, 2)
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");

%% Фильтр Чебышева 1 рода, s1 + s2 + s3
s = s1 + s2 + s3;

subplot(4, 1, 1);
plot(t, s);
legend("s");

n = 4;
Rp = 0.1;
[z, p, k] = cheb1ap(n, Rp);     
[b, a] = zp2tf(z, p, k);

w1 = 0.05;
w2 = 0.15;
w0 = sqrt(w1 * w2);
Bw = w2 - w1;
[b1, a1] = lp2bp(b, a, w0, Bw);    
f = abs(filter(b1, a1, t));
sf = s1 + s2.*f + s3.*f;
subplot(4, 1, 2)
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");

%% Фильтр Чебышева 2 рода, s1 + s2 + s3
s = s1 + s2 + s3;

subplot(4, 1, 1);
plot(t, s);
legend("s");

n = 4;
Rs = 45;
[z, p, k] = cheb2ap(n, Rs);
[b, a] = zp2tf(z, p, k);

w1 = 0.05;
w2 = 0.1;
w0 = 2 * pi * sqrt(w1 * w2);
Bw = 2 * pi * (w2 - w1);
[b2, a2] = lp2bs(b, a, w0, Bw);   
f = abs(filter(b1, a1, t));
sf = s1.*f + s2.*f + s3;
subplot(4, 1, 2)
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");

%% Эллиптический фильтр, s1 + s2 + s3
s = s1 + s2 + s3;

subplot(4, 1, 1);
plot(t, s);
legend("s");

n = 4;
Rp = 0.1;
Rs = 45;
w0 = 0.05;
[z, p, k] = ellipap(n, Rp, Rs);
[b, a] = zp2tf(z, p, k);

[b1, a1] = lp2lp(b, a, w0);      
f = abs(filter(b1, a1, t));
sf = s1.*f + s2 + s3;
subplot(4, 1, 2)
plot(t, sf);
legend("Результат фильтрации");

N_s = length(s);
ft = fft(s);
frequencies = (0:N_s-1)*(sr/N_s);
subplot(4, 1, 3)
plot(frequencies(1:31), ft(1:31))
legend("Спектр исходного сигнала");

N_sf = length(sf);
ftf = fft(sf);
frequencies = (0:N_sf-1)*(sr/N_sf);
subplot(4, 1, 4)
plot(frequencies(1:31), ftf(1:31))
legend("Спектр отфильтрованного сигнала");