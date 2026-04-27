import { View, Text, Pressable } from 'react-native';
import { useRouter } from 'expo-router';

export default function Home() {
  const router = useRouter();

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>OryxGo</Text>
      <Pressable onPress={() => router.push('/tour')}>
        <Text style={{ fontSize: 18, color: 'blue' }}>Start Tour</Text>
      </Pressable>
    </View>
  );
}
