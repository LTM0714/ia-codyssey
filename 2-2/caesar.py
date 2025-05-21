FILE_NAME = '2-2/password.txt'
RESULT_FILE = '2-2/result.txt'

def caesar_cipher_decode(target_text):
    # 알파벳 정의
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    len_alphabet = len(alphabet)
    
    # 모든 가능한 시프트 값에 대해 시도
    for shift in range(len_alphabet):
        decoded_text = ''

        for char in target_text:
            if char in alphabet:
                # .index() 메서드를 사용하여 현재 문자의 알파벳 인덱스 찾기
                index = alphabet.index(char)
                # 시프트 적용
                decoded_text += alphabet[(index - shift) % len_alphabet]
            elif char in alphabet.upper():
                # 대문자 처리
                index = alphabet.upper().index(char)
                decoded_text += alphabet.upper()[(index - shift) % len_alphabet]
            else:
                decoded_text += char  # 알파벳이 아닌 문자는 그대로 유지
        
        
        print(f'\n시프트 {shift}의 결과:')
        print(decoded_text)
        
        # 사용자에게 현재 결과가 올바른지 확인
        response = input('이 결과가 올바른가요? (y/n): ')
        if response.lower() == 'y' or response.lower() == 'yes':
            return shift, decoded_text
    
    return None, None


# password.txt 파일 읽기
def read_password():
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')
        return ''
    except Exception as e:
        print(f'파일을 읽는 중 오류가 발생했습니다: {e}')
        return ''

# result.txt에 저장하기
def save_result(encrypted_text, shift, result_text):
    try:
        with open(RESULT_FILE, 'w', encoding='utf-8') as file:
            file.write(f'원본 텍스트: {encrypted_text}\n')
            file.write(f'시프트 값: {shift}\n')
            file.write(f'해독된 텍스트: {result_text}\n')
        print('결과가 result.txt에 저장되었습니다.')
    except Exception as e:
        print(f'결과 저장 중 오류가 발생했습니다: {e}')


def main():
    # password.txt 파일 읽기
    encrypted_text = read_password()
    if not encrypted_text:
        return
    
    print('암호화된 텍스트: ', encrypted_text)
    print('\n각 시프트 값에 대한 디코딩 결과 확인')
    
    # 디코딩 시도
    shift, decoded_text = caesar_cipher_decode(encrypted_text)
    
    if shift is not None:
        # 결과를 result.txt에 저장
        save_result(encrypted_text, shift, decoded_text)
    else:
        print('모든 시프트 값을 시도했지만 올바른 결과를 찾지 못했습니다.')
        

if __name__ == '__main__':
    main()
