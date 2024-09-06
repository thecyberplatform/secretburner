import { ref, Ref } from 'vue';
import { LocalStorage } from 'quasar';

export const useCryptography = () => {
  const publicKey: Ref<string | undefined> = ref();
  const privateKey: Ref<string | undefined> = ref();

  async function generateKeyPair(): Promise<void> {
    const keyPair = await crypto.subtle.generateKey(
      {
        name: 'RSA-OAEP',
        modulusLength: 4096, // Key size in bits
        publicExponent: new Uint8Array([1, 0, 1]), // 0x010001 (common value for RSA keys)
        hash: 'SHA-256',
      },
      true,
      ['encrypt', 'decrypt']
    );

    publicKey.value = await exportPublicKey(keyPair.publicKey);
    privateKey.value = await exportPrivateKey(keyPair.privateKey);
  }

  async function exportPublicKey(publicKey: CryptoKey): Promise<string> {
    const keyData = await crypto.subtle.exportKey('spki', publicKey);
    const base64 = arrayBufferToBase64(keyData);
    return `-----BEGIN PUBLIC KEY-----\n${base64
      .match(/.{1,64}/g)
      ?.join('\n')}\n-----END PUBLIC KEY-----`;
  }

  async function importPublicKey(pem: string): Promise<CryptoKey> {
    // Remove the PEM header, footer and newlines
    const pemHeader = '-----BEGIN PUBLIC KEY-----';
    const pemFooter = '-----END PUBLIC KEY-----';
    const pemContents = pem
      .replace(pemHeader, '')
      .replace(pemFooter, '')
      .replace(/\s+/g, '');

    // Decode the base64 string to an ArrayBuffer
    const binaryDerString = atob(pemContents);
    const binaryDer = new Uint8Array(binaryDerString.length);
    for (let i = 0; i < binaryDerString.length; i++) {
      binaryDer[i] = binaryDerString.charCodeAt(i);
    }

    // Import the public key
    return await crypto.subtle.importKey(
      'spki',
      binaryDer.buffer,
      {
        name: 'RSA-OAEP',
        hash: 'SHA-256',
      },
      true,
      ['encrypt']
    );
  }

  function arrayBufferToBase64(buffer: ArrayBuffer): string {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
  }

  function base64ToArrayBuffer(base64: string): ArrayBuffer {
    const binaryString = window.atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
  }

  async function encryptData(
    publicKey: CryptoKey,
    plaintext: string
  ): Promise<string> {
    const encoder = new TextEncoder();
    const plaintextBuffer = encoder.encode(plaintext);
    const encryptedBuffer = await crypto.subtle.encrypt(
      { name: 'RSA-OAEP' },
      publicKey,
      plaintextBuffer
    );
    return arrayBufferToBase64(encryptedBuffer);
  }

  async function decryptData(
    privateKey: CryptoKey,
    encryptedBase64: string
  ): Promise<string> {
    const encryptedBuffer = base64ToArrayBuffer(encryptedBase64);
    const decryptedBuffer = await crypto.subtle.decrypt(
      { name: 'RSA-OAEP' },
      privateKey,
      encryptedBuffer
    );
    const decoder = new TextDecoder();
    return decoder.decode(decryptedBuffer);
  }

  async function exportPrivateKey(privateKey: CryptoKey): Promise<string> {
    const keyData = await crypto.subtle.exportKey('pkcs8', privateKey);
    const base64 = arrayBufferToBase64(keyData);
    return `-----BEGIN PRIVATE KEY-----\n${base64
      .match(/.{1,64}/g)
      ?.join('\n')}\n-----END PRIVATE KEY-----`;
  }

  async function importPrivateKeyPem(pem: string): Promise<CryptoKey> {
    const pemHeader = '-----BEGIN PRIVATE KEY-----';
    const pemFooter = '-----END PRIVATE KEY-----';

    const base64 = pem
      .replace(pemHeader, '')
      .replace(pemFooter, '')
      .replace(/\s+/g, '');

    const binaryDer = window.atob(base64);
    const binaryDerBytes = new Uint8Array(binaryDer.length);

    for (let i = 0; i < binaryDer.length; i++) {
      binaryDerBytes[i] = binaryDer.charCodeAt(i);
    }

    return crypto.subtle.importKey(
      'pkcs8',
      binaryDerBytes.buffer,
      { name: 'RSA-OAEP', hash: 'SHA-256' },
      true,
      ['decrypt']
    );
  }

  async function simpleEncrypt(
    message: string,
    passphrase: string
  ): Promise<string> {
    const iv = await deriveIv(passphrase);
    const key = await deriveKey(passphrase);

    const encoder = new TextEncoder();
    const data = encoder.encode(message);

    const encrypted = await crypto.subtle.encrypt(
      { name: 'AES-CBC', iv: iv },
      key,
      data
    );

    return bufferToHex(encrypted);
  }

  async function simpleDecrypt(
    encryptedMessage: string,
    passphrase: string
  ): Promise<string> {
    const iv = await deriveIv(passphrase);
    const key = await deriveKey(passphrase);

    const encryptedData = hexToBuffer(encryptedMessage);

    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-CBC', iv: iv },
      key,
      encryptedData
    );

    const decoder = new TextDecoder();
    return decoder.decode(decrypted);
  }

  async function deriveKey(passphrase: string): Promise<CryptoKey> {
    const encoder = new TextEncoder();
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      encoder.encode(passphrase),
      { name: 'PBKDF2' },
      false,
      ['deriveKey']
    );

    return crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: new Uint8Array(16), // Using a fixed salt since none is shared
        iterations: 100000,
        hash: 'SHA-256',
      },
      keyMaterial,
      { name: 'AES-CBC', length: 256 },
      false,
      ['encrypt', 'decrypt']
    );
  }

  async function deriveIv(passphrase: string): Promise<Uint8Array> {
    const encoder = new TextEncoder();
    const hash = await crypto.subtle.digest(
      'SHA-256',
      encoder.encode(passphrase)
    );
    return new Uint8Array(hash).slice(0, 16); // First 16 bytes as IV
  }

  function bufferToHex(buffer: ArrayBuffer): string {
    return [...new Uint8Array(buffer)]
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('');
  }

  function hexToBuffer(hex: string): ArrayBuffer {
    const typedArray = new Uint8Array(
      hex.match(/.{1,2}/g)?.map((byte) => parseInt(byte, 16)) || []
    );
    return typedArray.buffer;
  }

  function clearLocalPrivateKeys() {
    for (const localKey of LocalStorage.getAllKeys()) {
      if (localKey.startsWith('sbpvk')) {
        try {
          const burnAt: number = parseInt(localKey.split(':')[2]);
          const jsNow: number = Math.floor(Date.now() / 1000);

          // remove expired secrets
          if (jsNow > burnAt) {
            LocalStorage.removeItem(localKey);
          }
        } catch (err) {
          // delete any secret that is malformed.
          LocalStorage.removeItem(localKey);
        }
      }
    }
  }

  return {
    generateKeyPair,
    exportPublicKey,
    encryptData,
    decryptData,
    exportPrivateKey,
    importPrivateKeyPem,
    publicKey,
    privateKey,
    importPublicKey,
    simpleEncrypt,
    simpleDecrypt,
    clearLocalPrivateKeys,
  };
};
