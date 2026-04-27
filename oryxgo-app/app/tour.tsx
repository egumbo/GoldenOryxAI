import { useEffect, useState } from 'react';
import { View, Text, Pressable } from 'react-native';
import * as Location from 'expo-location';
import * as Speech from 'expo-speech';

export default function Tour() {
  const [story, setStory] = useState<any>(null);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;

      let location = await Location.getCurrentPositionAsync({});

      const res = await fetch('http://127.0.0.1:8000/tour/nearby', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          latitude: location.coords.latitude,
          longitude: location.coords.longitude,
          radius: 1000
        })
      });

      const data = await res.json();
      setStory(data);
      Speech.speak(data.narration);
    })();
  }, []);

  if (!story) return <Text>Loading...</Text>;

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 20 }}>{story.landmark}</Text>
      <Text style={{ marginTop: 10 }}>{story.narration}</Text>

      <Pressable onPress={() => Speech.speak(story.narration)}>
        <Text style={{ marginTop: 20, color: 'blue' }}>Replay Audio</Text>
      </Pressable>
    </View>
  );
}
