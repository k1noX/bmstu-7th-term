A_1 =    0.2;
omega_1 =   120;
phi_1 =  100;

A_2 =    1;
omega_2 =   18;
phi_2 =  0;

A_3 =    0.7;
omega_3 =   30;
phi_3 =  -60;

A_4 =    0.45;
omega_4 =   60;
phi_4 =  40;


sr = 2500;
step = 1/sr;
t = (0:step:1);

S1 = A_1*sin(2*pi*omega_1*t + phi_1);
S2 = A_2*sin(2*pi*omega_2*t + phi_2);
S3 = A_3*sin(2*pi*omega_3*t + phi_3);
S4 = A_4*sin(2*pi*omega_4*t + phi_4);

S = S1 .* (S2 + S3) .* S4;

N_s = length(S);
ft = abs(fft(S));
[pks, locs] = findpeaks(ft);

frequencies = (0:N_s-1)*(sr/N_s);

h = zeros(length(locs) + 1, 1);
h(2) = subplot(length(locs)/2 + 1, 2, 2);
plot(t, S);
h(1) = subplot(length(locs)/2 + 1, 2, 1);
plot(frequencies(1:150), ft(1:150));

n = 4;
for i = 1:length(locs)/2
    [b, a] = butter(n, [locs(i)*0.92/(sr/2) locs(i)*1.08/(sr/2)], 'bandpass');
    f = filter(b, a, S);

    N_f = length(f);
    ftf = abs(fft(f));
    frequencies = (0:N_f-1)*(sr/N_f);
    h(i*2 + 1) = subplot(length(locs)/2 + 1, 2, i*2 + 1);
    plot(frequencies(1:150), ftf(1:150))

    ftfi = ifft(ftf);
    h(i*2 + 2) = subplot(length(locs)/2 + 1, 2, i*2 + 2);
    plot(t, ftfi)
end
title(h(1), 'Спектр сигнала')
title(h(2), 'Обратное ДПФ сигнала')