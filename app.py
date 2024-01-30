import argparse
import pathlib
import time
from ultralytics import YOLO

if __name__ == '__main__':
    start_time = time.time()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='yolov8x.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='sample.mp4', help='path to data file or dataset folder, check https://docs.ultralytics.com/modes/predict/#inference-sources')
    parser.add_argument('--conf', type=float, default=0.01, help='object confidence threshold')
    parser.add_argument('--verbose', action='store_true', help='print detailed results')
    args = parser.parse_args()
    
    # Load a pretrained YOLOv8n model
    model = YOLO(args.model)
    
    # Run inference on the source
    results = model(args.source, conf=args.conf, stream=True, verbose=args.verbose)  # generator of Results objects
    ofstream = None
    frame_idx = 1
    for result in results:
        path = pathlib.Path(result.path)
        
        if ofstream is None:
            ofstream = open(path.with_suffix('.txt'), 'w')
        elif pathlib.Path(ofstream.name).stem != path.stem:
            ofstream.close()
            ofstream = open(path.with_suffix('.txt'), 'w')
            frame_idx = 1
        
        for box in result.boxes:
            cls = box.cls # shape: [1]
            conf = box.conf # shape: [1]
            xyxy = box.xyxy # shape: [1, 4]
            
            cls = int(cls)
            conf = float(conf)
            xyxy = xyxy[0].tolist()
            
            bbox = f'{cls},{conf},{xyxy[0]},{xyxy[1]},{xyxy[2]},{xyxy[3]}'
            ofstream.write(f'{frame_idx}, {cls}, {conf}, {xyxy[0]}, {xyxy[1]}, {xyxy[2]}, {xyxy[3]}\n')   
        frame_idx += 1

    if ofstream is not None and not ofstream.closed:
        ofstream.close()
    
    end_time = time.time()
    
    print(f'Model: {args.model}')
    print(f'Source: {args.source}')
    print(f'Inference time: {end_time - start_time} seconds')