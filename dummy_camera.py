from socketserver import BaseRequestHandler, UDPServer
import time

def bytes_to_str(bytes: bytes):
    '''Converts bytes to a printable string'''
    hex_bytes = bytes.hex()
    formatted = ' '.join(
        [hex_bytes[i:i + 2] for i in range(0, len(hex_bytes), 2)]
    )
    return formatted.upper()

class Handler(BaseRequestHandler):

    count = 0
    # Skip acknowledgement for every nth request
    skip_nth_ack = 0
    # Delay before sending acknowledgement
    ack_processing_delay = 0.05
    # Skip completion message for every nth request
    skip_nth_completion = 0
    # Delay before sending completion message
    completion_processing_delay = 0.05

    def handle(self):
        Handler.count += 1
        data, socket = self.request

        sequence_number = int.from_bytes(data[4:8], 'big')
        print(f'Command {sequence_number} received: {bytes_to_str(data)}')

        if not Handler.skip_nth_ack or \
           not Handler.count % Handler.skip_nth_ack == 0:
            ack = (
                b'\x01\x11\x00\x03' + sequence_number.to_bytes(4, 'big') + b'\x90\x41\xFF'
            )
            if Handler.ack_processing_delay:
                time.sleep(Handler.ack_processing_delay)
            socket.sendto(ack, self.client_address)
            print(
                f'Acknowledgement for command {sequence_number} sent: '
                f'{bytes_to_str(ack)}'
            )

        if not Handler.skip_nth_completion or \
           not Handler.count % Handler.skip_nth_completion == 0:
            completion = (
                b'\x01\x11\x00\x03' +
                sequence_number.to_bytes(4, 'big') +
                b'\x90\x51\xFF'
            )
            if Handler.completion_processing_delay:
                time.sleep(Handler.completion_processing_delay)
            socket.sendto(completion, self.client_address)
            print(
                f'Completion message for command {sequence_number} sent: '
                f'{bytes_to_str(completion)}'
            )

if __name__ == '__main__':
    HOST, PORT = '', 52381
    with UDPServer((HOST, PORT), Handler) as server:
        server.serve_forever()
