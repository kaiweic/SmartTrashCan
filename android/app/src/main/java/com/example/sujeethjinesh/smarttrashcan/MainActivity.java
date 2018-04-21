package com.example.sujeethjinesh.smarttrashcan;


import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.provider.MediaStore;
import android.support.v4.content.res.ResourcesCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

//import com.clarifai.api.ClarifaiClient;
//import com.clarifai.api.RecognitionRequest;
//import com.clarifai.api.RecognitionResult;
//import com.clarifai.api.Tag;

import com.clarifai.api.Tag;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import clarifai2.api.ClarifaiBuilder;
import clarifai2.api.ClarifaiClient;
import clarifai2.api.ClarifaiResponse;
import clarifai2.dto.input.ClarifaiInput;
import clarifai2.dto.model.output.ClarifaiOutput;
import clarifai2.dto.prediction.Concept;

public class MainActivity extends AppCompatActivity {

    Button analyzeButton;
    ImageView destinationImageView;
    static final int CAM_REQUEST = 1;
//    private final ClarifaiClient clarifaiClient = new ClarifaiClient(Credentials.CLIENT_ID,
//            Credentials.CLIENT_SECRET);
    private final ClarifaiClient clarifaiClient = new ClarifaiBuilder(Credentials.CLARIFAI_API_KEY).buildSync();
    ArrayList<String> items;
    TextView outputTextView;

    Set<String> recyclables;
    Set<String> compostables;
    Set<String> landfill;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        analyzeButton = (Button) findViewById(R.id.analyze_button);
        destinationImageView = (ImageView) findViewById(R.id.destination_image_view);
        outputTextView = (TextView) findViewById(R.id.output_text_view);

        recyclables = new HashSet<>(Arrays.asList("bottle", "plastic"));
        compostables = new HashSet<>(Arrays.asList("apple", "clementine", "orange", "fruit", "tangerine", "mandarin", "food", "banana", "coffee", "cup"));
        landfill = new HashSet<>(Arrays.asList("phone", "wrapper"));

        items = new ArrayList<>();
        if (checkSelfPermission(Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {

            requestPermissions(new String[]{Manifest.permission.CAMERA},
                    CAM_REQUEST);
        }

        final Context context = this.getApplicationContext();
        analyzeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                if (cameraIntent.resolveActivity(getPackageManager()) != null) {
                    startActivityForResult(cameraIntent, CAM_REQUEST);
                }
            }
        });
    }

    private File getFile() {
        File folder = new File("sdcard/camera_app");

        if (!folder.exists()) {
            folder.mkdir();
        }
        File image_file = new File(folder, "cam_image.jpg");
        return image_file;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (data != null && resultCode == RESULT_OK && requestCode == CAM_REQUEST) {
            Bitmap bitmap = (Bitmap) data.getExtras().get("data");
            destinationImageView.setImageBitmap(bitmap);

            // Run recognition on a background thread.
            new AsyncTask<Bitmap, Void, ClarifaiResponse<List<ClarifaiOutput<Concept>>>>() {
                @Override
                protected ClarifaiResponse<List<ClarifaiOutput<Concept>>> doInBackground(Bitmap... bitmaps) {
                    ByteArrayOutputStream stream = new ByteArrayOutputStream();
                    bitmaps[0].compress(Bitmap.CompressFormat.JPEG, 90, stream);
                    byte[] byteArray = stream.toByteArray();
                    return clarifaiClient.getDefaultModels().generalModel().predict().withInputs(ClarifaiInput.forImage(byteArray)).executeSync();
//                    return clarifaiClient.recognize(new RecognitionRequest(byteArray).setModel("general-v1.3")).get(0);
                }

                @Override
                protected void onPostExecute(ClarifaiResponse<List<ClarifaiOutput<Concept>>> result) {
                    boolean found = false;
                    String foundText = "Trash :(";
                    for (Concept tag : result.getOrNull().get(0).data()) {
                        System.out.println(tag.name());
                        if (recyclables.contains(tag.name())) {
                            foundText = "Recycle! :)";
                            outputTextView.setTextColor(ResourcesCompat.getColor(getResources(), R.color.pukeGreen, null));
                            found = true;
                        } else if (compostables.contains(tag.name())) {
                            foundText = "Compost! :)";
                            outputTextView.setTextColor(ResourcesCompat.getColor(getResources(), R.color.blue, null));
                            found = true;
                        } else if (landfill.contains(tag.name())) {
                            foundText = "Trash! :(";
                            outputTextView.setTextColor(ResourcesCompat.getColor(getResources(), R.color.heartRed, null));
                            found = true;
                        }
                    }
                    if (!found) {
                        foundText = "Trash! :(";
                        outputTextView.setTextColor(ResourcesCompat.getColor(getResources(), R.color.heartRed, null));
                    }
                    outputTextView.setText(foundText);
                }
            }.execute(bitmap);
        }
    }
}
